# FileMo
CS441 group project  

## format:
* all ifs end in a :

### path format: /path/
* ex:
	* /files/
	* /long/files/
	* /memes/jpg/

### name filtering:
* exact match
	* filename (!=,=) string
* match
	* filename.contains (!=,=) string
		* filename:
			* name: compare to file name
			* type: compare to file type
		* string: "user input" or 'user input'
* ex:
	* name = "hello world":			
		* if file name is hello world
	* type != 'mp4':
		* if file type is not mp4
	* name.contains != 'file': 
		* if filename does not contain the string file

### date filtering:
* filedate (!=,=,<,<=,>,>=) userdate
	* filedate:
		* modifydate
		* createdate
		* accessdate
	* userdate:
		* date: mm-dd-yyyy, compare to date, leading 0 on single digit dates
		* time: integer followed by s(seconds),mn(minutes),h(hours),d(days),m(months),y(years), copare to time ago
* ex:
	* modifydate > 01-19-2005:
		* if file modifydate since jan 19 2005
	* createdate != 35d: 
		* if file createdate not 35 days ago

### size filtering:

* size (!=,=,<,<=,>,>=) usersize
	* size
	* usersize: integer followed by b(bytes),kb(kilobytes),mb(megabytes),gb(gigabytes),tb(terabytes)
* ex:
	* size <= 234mb:
		* if file less than or equal to 234 megabytes
	* size > 4gb:
		* if file greater than 4 gigabytes