This script reads data from 3 files. 2 of them contain information with abbreviations of racers, their start and end time of best lap in Monaco race.
3-rd file contains information with abbreviation of racer, his name and team.
Script work with all this data and orders racers by time and print report that shows the top 15 racers and the rest after underline, for example:


1. Daniel Ricciardo      | RED BULL RACING TAG HEUER     | 1:12.013

2. Sebastian Vettel      | FERRARI                                            | 1:12.415

3. ...

------------------------------------------------------------------------

16. Brendon Hartley   | SCUDERIA TORO ROSSO HONDA | 1:13.179

17. Marcus Ericsson  | SAUBER FERRARI| 1:13.265


Start page index '/' returns information how to use this app.


You can get total data with using next URL: /report.
Returns full report about results of Monaco Race 2018. You also can choose type of sorting of this report in next format:
/report?order=asc or /report?order=desc


"/report/drivers" - returns list of racers in next format:
    {name} {abbreviatiom}
    Abbreviations are active links to full data about driver



"/report/<string:code>" returns full data about driver if you click to his code in /report/drivers



/api/v1/report/ - creates api for getting an order. You can choose json or xml formats: for example /api/v1/report/?format=xml

