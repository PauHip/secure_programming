Secure Programming
Exercise work report

This app is a code static analyser that can tell if the code has risk to Sql injection attack. It does it by studying if query parameterization is used in all Sql clauses of the code.

At this stage, this program can analyse php code. It uses command line interface that is used in Linux command line by writing:
python main.py <filename>
where <filename> refers to the file that ends with .php. The program tells if it finds an unknown file type.

The php code must start with <?php> tag and end with ?> tag. The ending tag must be placed so that after it there isn't any other code because the program takes the whole line where the ending tag is. If after the ending tag there would be something, then    the analysis could contain the code that isn't Php. The comments are allowed, using //, # or multiline /*--*/ notation. The */ symbol has to be last on its line, or alone, in the same way as the php ending tag, because the program removes the comment lines from its analysis. In practice these limitations means the following:

Allowed:
<?php
$var1 = 12;
?>
<?php $var2 = 15; ?>
<?php */ This is
a multiline comment */ ?>
<?php /* Another
multiline comment */
$var2 = 17; ?>

Not allowed:
<?php $var1 = 12;
?> <h1>Test</h1>
<?php /* This is
a multiline comment */ $var1 = 12 ?>

Allowed Sql commands that this app identifies are "select", "insert into", "drop", "create table", "alter table", "alter column", "delete from" and "update". Sql queries must be closed in double quotes ("). Multiline queries are allowed. The commands aren't case sensitive. The following means the same:
<?php $query1 = pg_query("select * from students;");?>
<?php $query1 = pg_query = "SELECT *
FROM students;");?>
Nested commands are allowed as well: 
<?php $query2 = pg_query("select * from
(select name from students);"); ?>

When binding parameters, it is expected that the bound parameter is inside single quotes (') and that bindParam clause is used. On other words, it is expected that the parameter binding is used by writing bindParam(':name', $name) or bindParam(':name', "John") (double quotes are allowed after the bound parameter). Instead it isn't allowed to write bindParam(":name", $name).

The structure of the program consists of main file and the classes. There is a base class called Analyse_base that has methods for finding an Sql queries and checking if the given query is wulnerable to Sql injections or not. Then there is the class PhpAnalyser that inherits this class. In addition of this and some private methods, it has a public method called find_php_code whose purpose is to remove those lines that are not php code, to diminish the possibility that the program says that such rows are wulnerable that cannot even contain php code. Then there is the main.py file that reads the file and selects the suitable object (this is done because of the possibility to expand to more languages to analyse). In addition, the main file prints the results of the analyser.

Security

SANS25 Checklist
1. Out-of-bounds Write [1]. It isn't propably no problem because of Python [1].
2. Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') [2]. It isn't  a problem because this isn't a web page or application.
3. Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') [3]. The whole purpose of this program is to prevent such situations but the program itself doesn't cause them because it doesn't communicate with Sql database.
4. Improper Input Validation [4]. The program checks if the file exists and filetype is such that it identifies it and gives an error if something is wrong.
5. Out-of-bounds Read [5]. This is propably not problem in Python [5].
6. Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') [6]. I am not sure about this but maybe not a problem, this isn't a web application, I don't execute any command directly and have limited the number of possible command line parameters to one although I don't know if it actually effects that problem.
7. Use After Free [7]. This is not a problem because I don't use manual memory handling so the system decides when to free memory.
8. Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') [8]. I think this isn't a problem. I considered to put the condition that checks that the slash (/) or backslash (\) characters aren't used in filenames to avoid the situation where an users have access to some file they aren't allowed to see. However, I thought that this isn't necessary  because this program doesn't do anything about the file it reads. Of course someone could open some file that contains some private data. However, this can be done without this app as well if the user has rights to see the files of the computer and if doesn't, then this app doesn't change the situation. So I consider that this isn't a problem.
9. Cross-Site Request Forgery (CSRF) [9]. This is not a problem because this isn't a web page or application.
10. Unrestricted Upload of File with Dangerous Type [10]. This is not possible because I check that the filetype is known. I addition, Python program can't run php files. If I would expand my analyser to analyse Python programs the question might occur but it couldn't still be a problem because my program only reads the file without running it.
11. NULL Pointer Dereference [11]. This is not a problem because as far as I know Python has no pointers and if it has, I haven't used them.
12. Deserialization of Untrusted Data  [12]. I have quite sure I haven't used data serialization. It apparently means packaging data or object for store [12], and I think I haven't done such thing so this isn't a problem.
13. Integer Overflow or Wraparound [13]. Seemingly this isn't problem in Python. Python documentation says that overflowing errors don't happen with integers, except seemingly in some situations where the integers go outside required range [14] and this propably doesn't happen in my code because I've used ranges only with list indexing and don't know any other situations where I could use some range that could be exceeded.
14. Improper Authentication [15]. This isn't a problem because my app has no authentication. Of course I could have added it but I think it isn't necessary for this app.
15. Use of Hard-coded Credentials [16]. It seems this relates to authentication matters so it isn't problem with my app.
16. Missing Authorization [17]. My app has no resources that require authorisation so this isn't a problem.
17. Improper Neutralization of Special Elements used in a Command ('Command Injection') [18]. Propably this isn't a problem. I've limited the numbers of parameters that can be given in command line, and my program don't run them. It only reads files, and as previously mentioned, I considered that it is no need for limit this action. An attacker can't therefore give the command using command line because the command line input is handled as filename, or give the commands in the file because my program only reads the file without running it.
18. Missing Authentication for Critical Function [19]. This isn't a problem because I have no authentication, and as mentioned earlier, I think there is no need for it.
19. Improper Restriction of Operations within the Bounds of a Memory Buffer [20]. This isn't a problem with Python [20 0].
20. Incorrect Default Permissions [21]. This shouldn't be a problem because I don't install anything, only import some modules that are build in Python and one of my own. Of course someone could maybe change them but not without the access to the source code, and propably I can't do anything with that problem because it is with all programs.
21. Server-Side Request Forgery (SSRF) [22]. This isn't a web page so this problem shouldn't occur.
22. Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') [23] This isn't a problem  because I don't use concurrency.
23. Uncontrolled Resource Consumption [24]. I have added a MemoryError handler to the file reading function where I think it is the only situation some resource error would happen, and closed the file afterwards so it can't consume resources.
24. Improper Restriction of XML External Entity Reference [25] This isn't a problem because my program doesn't use Xml files.
25. Improper Control of Generation of Code ('Code Injection') [26]. This is not a problem because user isn't allowed to write code.

In  addition of these things, I have encoded the contents of the file the program analyses to UTF-8, after understanding that if I search things from the file, it can cause wrong results if the codings of my code and the file are different. I don't, however, know how useful this actually is because after trying I noticed that  at least UCS-2 coding doesn't work. But hopefully this arrangement has some use.

I haven't done much security testing. I have made sure that my error messages work, which means that it isn't possible to give unknown filename or filetype. I also tried the working of my encoding arrangement with ansi and UTF-8-bom and it worked correctly, or at least that test file that I used worked correctly. As mentioned, I tried the UCS-2 coding, both Be Bom and Le Bom versions and they didn't work. I used these codings because I used Notepad++ and they were available there. I tried also to give directory path, such as ../../file.txt to see if the program accepts it. It did and I decided to allow it    (see checklist point 8).

The following  things to be added would be to do corresponding analysis to other languages. I thought Python but didn't implement it because of the limited time. But this program is built so that it is rather easy to expand it. More wulnerabilities could be added as well, they would come to the Analyser_base class and from there inherited to the different languages. Of course, some languages could have their own wulnerabilities, and then they are put to the class of the language instead of the base class.

References
[1] CWE - CWE-787: Out-of-bounds Write (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/787.html. referred in 24.5.2023
[2] CWE - CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/79.html. referred in 24.5.2023
[3] CWE - CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/89.html. referred in 24.5.2023
[4] CWE - CWE-20: Improper Input Validation (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/20.html. referred in 24.5.2023
[5] CWE - CWE-125: Out-of-bounds Read (4.11) (2023). SANS Institute. Institutehttps://cwe.mitre.org/data/definitions/125.html. referred in 24.5.2023
[6] CWE - CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/78.html, referred in 24.5.2023
[7] CWE - CWE-416: Use After Free (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/416.html. referred in 25.5.2023
[8]CWE - CWE-787: Out-of-bounds Write (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/787.html. referred in 25.5.2023
[9] CWE - CWE-352: Cross-Site Request Forgery (CSRF) (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/352.html. referred in 25.5.2023
[10] CWE - CWE-434: Unrestricted Upload of File with Dangerous Type (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/434.html. referred in 25.5.2023
[11] CWE - CWE-476: NULL Pointer Dereference (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/476.html. referred in 25.5.2023
[12] CWE - CWE-502: Deserialization of Untrusted Data (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/502.html. referred in 25.5.2023
[13]  CWE - CWE-190: Integer Overflow or Wraparound (4.11). SANS Institute. https://cwe.mitre.org/data/definitions/190.html. referred i 25.5.2023
[14] Built-in Exceptions (2023). Python 3.7 documentation. DevDocs. https://devdocs.io/python~3.7/library/exceptions#concrete-exceptions. referred i 25.5.2023
[15] CWE - CWE-287: Improper Authentication (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/287.html. referred i 25.5.2023
[16] CWE - CWE-798: Use of Hard-coded Credentials (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/798.html. referred i 25.5.2023
[17] CWE - CWE-862: Missing Authorization (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/862.html. referred i 25.5.2023
[18] CWE - CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/77.html. referred i 25.5.2023
[19] CWE - CWE-306: Missing Authentication for Critical Function (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/306.html. referred i 25.5.2023
[20] CWE - CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer (4.11) (2023). SANS Institute.  https://cwe.mitre.org/data/definitions/119.html. referred i 26.5.2023
[21] CWE - CWE-276: Incorrect Default Permissions (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/276.html. referred i 25.5.2023
[22] CWE - CWE-918: Server-Side Request Forgery (SSRF) (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/918.html. referred i 25.5.2023
[23] CWE - CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/362.html. referred i 25.5.2023
[24] CWE - CWE-400: Uncontrolled Resource Consumption (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/400.html. referred i 25.5.2023
[25] CWE - CWE-611: Improper Restriction of XML External Entity Reference (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/611.html. referred i 25.5.2023
[26] CWE - CWE-94: Improper Control of Generation of Code ('Code Injection') (4.11) (2023). SANS Institute. https://cwe.mitre.org/data/definitions/94.html. referred i 25.5.2023