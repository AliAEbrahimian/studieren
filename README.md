[🇬🇧 English](README.md) | [🇮🇷 فارسی](README_fa.md) | [🇩🇪 Deutsch](README_de.md)

...


<h1 align="left">Hi...! What's up?🙋‍♂️</h1>

###

<p align="left">I am Ali and I program on the web, from Iran.🧑‍💻</p>

###

<h2 align="left">About me</h2>

###

<p align="left">My mother tongue is Persian and I am learning German (I have a B2 German language certificate!)😊👌<br>I want to work in a good company in Germany.💪✊<br>My hobbies are game development and video games.🎲🎮🕹️</p>

###

<h2 align="left">I code with</h2>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" height="33" alt="java logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="33" alt="python logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="33" alt="html5 logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="33" alt="css logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="33" alt="javascript logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" height="33" alt="bootstrap logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg" height="33" alt="kotlin logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/android/android-original.svg" height="33" alt="android logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/androidstudio/androidstudio-original.svg" height="33" alt="androidstudio logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vagrant/vagrant-original.svg" height="33" alt="vagrant logo"  />
  <img width="6" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" height="33" alt="github logo"  />
</div>

###

<div align="left">
  <a href="https:/www.linkedin.com/in/ ali-aghaebrahimian/" target="_blank">
    <img src="https://img.shields.io/static/v1?message=LinkedIn&logo=linkedin&label=&color=0077B5&logoColor=white&labelColor=&style=flat" height="27" alt="linkedin logo"  />
  </a>
  <a href="https://www.instagram.com/amzegon?igsh=bHBlbnRvd2JlYmF0" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Instagram&logo=instagram&label=&color=E4405F&logoColor=white&labelColor=&style=flat" height="27" alt="instagram logo"  />
  </a>
  <a href="mailto:2aaghaebrahimian@gmail.com" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Gmail&logo=gmail&label=&color=D14836&logoColor=white&labelColor=&style=flat" height="27" alt="gmail logo"  />
  </a>
  <a href="https://t.me/AliAEbrahimian" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Telegram&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=flat" height="27" alt="telegram logo"  />
  </a>
</div>

###

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=AliAEbrahimian&hide_title=false&hide_rank=false&show_icons=true&include_all_commits=true&count_private=true&disable_animations=false&theme=dracula&locale=en&hide_border=false&order=1" height="150" alt="stats graph"  />
  <img src="https://github-readme-stats.vercel.app/api/top-langs?username=AliAEbrahimian&locale=en&hide_title=false&layout=compact&card_width=320&langs_count=5&theme=dracula&hide_border=false&order=2" height="150" alt="languages graph"  />
</div>

###

Project: Studieren – Language School Management System
Overview
A comprehensive web-based management platform for a language institute built with Django. The system supports 7 user roles with fine-grained access control and covers course management, enrollment, attendance, exams, placement tests, feedback, finance, messaging, a shop, and gamification.

Tech Stack

Backend: Django 5.2, Python 3.13

Database: PostgreSQL (production), SQLite (development)

Frontend: Django Templates + SCSS

Auth: Email-based, 7 roles

Payments: Real payment gateway

Testing: pytest with high coverage

Reporting: Interactive charts (Chart.js), PDF/Excel export

User Roles
Student, Teacher, Education Manager, Senior Manager, Staff, Exam Corrector, Exam Manager

Key Features (All Implemented)

Course & Class Management: CRUD for courses and in-person/online classes, weekly scheduling, auto-generated class codes and sessions, tuition settings.

Enrollment & Transfers: Student self-enrollment with a 3-day grace period, withdrawal and transfer requests with manager approval, automatic fee difference and tax calculation.

Attendance: Interactive matrix with 4 statuses (Present, Absent, Late, Excused), future sessions locked, Excel export.

Exams & Grading: Written and oral exams with dynamic sections, grade entry by correctors/managers, finalization with grade locking, student grade appeal workflow with manager review.

Placement Tests: Test request, fee payment, request management, result recording.

Class Feedback: Student evaluations of teachers (5 criteria), anonymous average ratings shown to teachers.

Finance: Automatic invoices with configurable tax, payment tracking, receipts showing net amount, tax, and total.

Manager Reports: 5-tab dashboard (Finance, Academic, Attendance, Exams, Teacher Feedback) with interactive charts and PDF/Excel export.

User & Staff Management: Create users with any role, profile editing, deactivation, teacher assignment, 360° student and teacher profiles.

Notifications: Email and in-app alerts for enrollments, request approvals/rejections, grade postings, etc.

Internal Messaging: Message inbox among students, teachers, and staff.

Shop: Module for selling books and materials, with cart and checkout.

Gamification: Points, badges, and leaderboards to boost student engagement.

Security: Sensitive keys in .env, PostgreSQL in production, role checks on all views, atomic transactions for critical operations.

My Role

Requirements analysis aligned with educational standards (Moodle, Canvas)

Full backend design (models, views, URL routing)

Implementation of multi-role authentication and role-based access control

Frontend development using Django Templates and SCSS (no external CSS frameworks)

Integration of a real payment gateway and tax logic

Writing a comprehensive automated test suite with pytest

Development of advanced features: grade appeal, notifications, exportable reports, shop, gamification

Secure deployment and server configuration