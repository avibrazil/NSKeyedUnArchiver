# NSKeyedUnArchiver

Unserializes any binary|text|file|memory plist data and returns a usable Python dict.

Uses only Python 3.8 plistlib, no other dependencies.

Automatically converts well known data types to Python-equivalent data types:

- NSArray -> list
- NSMutableDictionary, NSDictionary -> dict
- NSMutableString, NSString -> unwrap the string
- NSMutableData, NSData -> unwrap the data
- NSDate -> datetime

Check [pypi](https://pypi.org/project/NSKeyedUnArchiver/) for packages.

License is LGPL 3.

## Sample usage

```python
import NSKeyedUnArchiver

file='/patch/to/file.plist'
my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(file)


data=b'bplist00\xd4\x01\.........'
my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(file)


data='<plist version="1.0">......'
my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(file)


file=PurePath('/patch/to/file.plist')
my_dict=NSKeyedUnArchiver.unserializeNSKeyedArchiver(file)
```