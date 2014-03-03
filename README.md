This software was written to run a small, panel-focused fan conference.  Specifically, [Intercon N][0]'s [Pre-convention][1].  The original site lived at [http://precon.free-dissociation.com][2].

[0]: http://www.interactiveliterature.org/N/
[1]: http://www.interactiveliterature.org/N/Thursday.php
[2]: http://precon.free-dissociation.com

It uses Django and Twitter Bootstrap, like half of everything else on the Internet.

The software should probably get a better name than 'precon' at some point -- not that it isn't descriptive, but it's confusing to overload the conference's nickname.

I wrote it on a great hurry because I couldn't figure out how to make [Symposion][3] work and needed to get a schedule out the door.  If you are interested in software with actual commercial support, which has been used to run actual open-source conferences, you might check Symposion out.

[3]: http://eldarion.com/symposion/

This software has a bunch of rough edges.  It's not really suited for use yet by people who aren't willing to modify the source when necessary.  Many things are hardcoded which should not be.  The process of turning panel proposals into accepted panels involves exporting the proposals as CSV using a management command, digesting them into accepted panels with panelist lists in some kind of spreadsheet program, and then importing the panelists and the accepted panels back in as two separate CSV files.  It is godawful ugly, but it was expedient.

Support is provided on a solidly best-effort basis.  Which is to say that you shouldn't assume I will respond to your e-mails.  I'm sorry.  I will try to respond!  But this isn't my day-job, and I am often hosed and distracted.  Pull requests and patches are also welcome, although the same caveat applies.  It's released under the MIT License, and if somebody wants to fork this and make a real open-source project with mailing lists and everything, go with my blessing.  (Just please don't call it 'precon'.)

Because, the bones of a more complete app are all right there.  The software provides:

* An attendee and prospective panelist survey, to gauge interest in various panel proposals.
* A an online schedule and panel list which uses Bootstrap and is therefore reasonably attractive and reasonably mobile-friendly.
* Basic user accounts for staff, because Django.
* Print-formatted schedules and room signs.
* Various scheduling views for staff, to make it easier to not eg. double-book panelists.  This was why I started writing software in the first place, because scheduling the conference the previous year in my head about gave me an aneurysm.

It should be easy to staple on a panel bid form and e-mail sending capabilities, I just haven't done it yet.

Some screenshots:

[![precon survey][precon survey]][precon survey]

[![precon schedule][precon schedule]][precon schedule]

[![precon panel list][precon panel list]][precon panel list]

[![precon schedule print][precon schedule print]][precon schedule print]

[![precon staff][precon staff]][precon staff]

[![precon admin][precon admin]][precon admin]

[precon survey]: https://github.com/kevinr/precon-project/raw/master/img/precon-survey.png
[precon schedule]: https://github.com/kevinr/precon-project/raw/master/img/precon-schedule.png
[precon panel list]: https://github.com/kevinr/precon-project/raw/master/img/precon-panel-list.png
[precon schedule print]: https://github.com/kevinr/precon-project/raw/master/img/precon-schedule-print.png
[precon staff]: https://github.com/kevinr/precon-project/raw/master/img/precon-staff.png
[precon admin]: https://github.com/kevinr/precon-project/raw/master/img/precon-admin.png

This installs basically like any other Django app, which is to say, the instructions from Daniel Greenfeld and Audrey Roy's excellent [Django starter template README][4] are still mostly correct.

[4]: https://github.com/kevinr/precon-project/blob/master/README.twoscoops-template.rst

Good luck.

- Kevin Riggle (kevinr@free-dissociation.com)
