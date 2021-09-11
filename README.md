# NSKeyedUnArchiver

Unserializes any binary|text|file|memory plist data and returns a usable Python dict.

Uses only Python 3.8 plistlib, no other dependencies.

Automatically converts well known data types to Python-equivalent data types:

- NSArray -> list
- NSMutableDictionary, NSDictionary -> dict
- NSMutableString, NSString -> unwrap the string
- NSMutableData, NSData -> unwrap the data
- NSDate -> datetime