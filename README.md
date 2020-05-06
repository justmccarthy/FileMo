# FileMo
CS441 group project

all ifs end in a :

path format: /path/
	ex:
		/files/
		/long/files/

name filtering:
	exact match
		filename (!=,=) string
	match
		filename.contains (!=,=) string
	filename:
		name: compare to file name
		type: compare to file type
	string: "user input" or 'user input'
	ex:
		name = "hello world":			if file name is hellow world
		type != 'mp4':					if file type is not mp4
		name.contains != 'file':		if filename does not contain the string file
date filtering:
	filedate (!=,=,<,<=,>,>=) userdate
	filedate:
		modifydate
		createdate
		accessdate
	userdate:
		date: dd-mm-yyyy, compare to date
		time: integer followed by s(seconds),mn(minutes),h(hours),d(days),m(months),y(years), copare to time ago
	ex:
		modifydate > 19-01-2005:		if file modifydate since jan 19 2005
		createdate != 35d:				if file createdate not 35 days ago
size filtering:
		size (!=,=,<,<=,>,>=) usersize
	size
	usersize: integer followed by b(bytes),kb(kilobytes),mb(megabytes),gb(gigabytes),tb(terrabytes)
	ex:
		size <= 234mb:		if file less than or equal to 234 megabytes
		size > gb:			if file greater than 4 gigabytes
		