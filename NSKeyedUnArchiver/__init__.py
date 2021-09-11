import copy
import datetime
import logging
import pathlib
import plistlib


__version__ = '1.2'

module_logger = logging.getLogger(__name__)



def _unserialize(o: dict, serialized: dict, removeClassName: bool, start: bool=True):
    if start:
        reassembled=copy.deepcopy(o)
    else:
        reassembled=o

    finished=False
    while not finished:
        finished=True

        cursor=None
        if isinstance(reassembled,bytes):
            try:
                return unserializeNSKeyedArchive(reassembled)
            except:
                # Not plist data, just plain binary
                return reassembled
        elif isinstance(reassembled,dict):
            cursor=reassembled.keys()
        elif isinstance(reassembled,list):
            cursor=range(len(reassembled))
        else: # str, int etc
            print("reassembled is a " + str(type(reassembled)) + ":" + str(reassembled))
            return reassembled




        for k in cursor:
#             print(f"cursor={k}")
            if isinstance(reassembled[k],plistlib.UID):
                reassembled[k]=copy.deepcopy(serialized[reassembled[k].data])

                if str(reassembled[k]) == '$null': reassembled[k]=None

                finished=False
            elif isinstance(reassembled[k],dict) or isinstance(reassembled[k],list):
                reassembled[k]=_unserialize(reassembled[k], serialized, start=False)

                if '$class' in reassembled[k] and '$classes' in reassembled[k]['$class']:
                    # Specialized handler for common class types

                    if 'NSArray' in reassembled[k]['$class']['$classes']:
                        reassembled[k]=reassembled[k]['NS.objects']

                    elif any(c in reassembled[k]['$class']['$classes'] for c in ['NSMutableDictionary','NSDictionary']):
                        reassembled[k]=dict(zip(reassembled[k]['NS.keys'],reassembled[k]['NS.objects']))

                    elif any(c in reassembled[k]['$class']['$classes'] for c in ['NSMutableString', 'NSString']):
                        reassembled[k]=reassembled[k]['NS.string']

                    elif any(c in reassembled[k]['$class']['$classes'] for c in ['NSMutableData', 'NSData']):
                        reassembled[k]=reassembled[k]['NS.data']

                    elif 'NSDate' in reassembled[k]['$class']['$classes']:
                        apple2001reference=datetime.datetime(
                            2001, 1, 1,
                            tzinfo=datetime.timezone.utc
                        )
                        reassembled[k]=datetime.datetime.fromtimestamp(
                            reassembled[k]['NS.time'] + apple2001reference.timestamp(),
                            datetime.timezone.utc
                        )

                    if removeClassName:
                        # Remove visual polution
                        del reassembled[k]['$class']

                finished=True

    return reassembled




def unserializeNSKeyedArchiver(plist, removeClassName=True):
    """
    plist can be:
    • PurePath   ⟹ open the file and plistlib.loads()
    • string     ⟹ check if its a file name, open it and plistlib.loads()
    • string     ⟹ try to read it as XML with plistlib.loads()
    • bytes      ⟹ pass it through plistlib.loads()
    • dict       ⟹ unserialize
    """


    if isinstance(plist,pathlib.PurePath):
        plistdata=plistlib.load(plist)
    elif isinstance(plist,str):
        try:
            # Try to open it as a file
            with open(plist,'rb') as f:
                plistdata=plistlib.load(f)
        except FileNotFound:
            # Try to parse it as plain (XML) text
            plistdata=plistlib.loads(plist)
    elif isinstance(plist,bytes):
            plistdata=plistlib.loads(plist)
    elif isinstance(plist,dict):
        # plist is already a plistlib-parsed dict
        plistdata=plist
    else:
        raise TypeError("Trying to plist-parse something that is neither a PurePath, file name, XML text, plist bytes stream nor a dict.")


    if '$top' in plistdata:
        o=copy.deepcopy(plistdata['$top'])
        unserialized=_unserialize(o,plistdata['$objects'], removeClassName)
    else:
        raise TypeError("Passed object is not an NSKeyedArchiver")

    if len(unserialized)==1 and 'root' in unserialized:
        # Unserialized data contains only 1 object, so no need to nest it under 'root'
        unserialized=unserialized['root']

    return unserialized

