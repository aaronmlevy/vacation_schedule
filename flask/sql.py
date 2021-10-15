from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)
mysql.connect()

cursor = mysql.get_db().cursor()

query = """ CREATE TABLE `call_schedule` (
          `date` DATE NOT NULL,
            `phx` varchar(255) NOT NULL,
              `mrct` varchar(255) NOT NULL,
              `cch` varchar(255) NOT NULL,
              `mini1` varchar(255) NOT NULL,
              `mini2` varchar(255) NOT NULL
        ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
"""

INSERT INTO `call_schedule` (`date`, `phx`, `mrct`, `cch`, `mini1`, `mini2`) VALUES
(date('2021-05-08'),'ls','ba','bs','mp','gg');
(date('2021-05-15'),ts,ak,rs,rr,mp),
(date('2021-05-22'),dm,sg,ag,rr,lp),
(date('2021-05-29'),je,ec,aa,mp,sh),
(date('2021-05-31'),je,ec,aa,mp,sh),
(date('2021-06-05'),sh,jg,eb,pp,gg),
(date('2021-06-12'),gg,pb,lk,pp,lp),
(date('2021-06-19'),je,sb,bs,ak,sk),
(date('2021-06-26'),ts,jg,sk,pb,eb),
(date('2021-07-03'),fd,sh,bj,pb,mp),
(date('2021-07-05'),fd,sh,bj,pb,mp),
(date('2021-07-10'),ec,ag,sb,pp,lp),
(date('2021-07-17'),je,ba,ts,pb,sk),
(date('2021-07-24'),ms,sh,bs,sk,mp),
(date('2021-07-31'),lk,aa,ss,pp,bj),
(date('2021-08-07'),ls,rs,sb,mp,bj),
(date('2021-08-14'),gg,ba,sk,rr,mp),
(date('2021-08-21'),fd,jg,ec,rr,lp),
(date('2021-08-28'),ls,pb,mh,mp,ak),
(date('2021-09-04'),rr,rs,bs,pb,ak),
(date('2021-09-06'),rr,rs,bs,pb,ak),
(date('2021-09-11'),je,ag,ss,pp,sh),
(date('2021-09-18'),ts,ak,sb,pp,bj),
(date('2021-09-25'),sg,ba,bs,mp,lp),
(date('2021-10-02'),dm,rr,fd,mp,pb),
(date('2021-10-09'),ms,ec,ts,eb,lp),
(date('2021-10-16'),ls,ag,bs,pp,bj),
(date('2021-10-23'),mh,sg,ss,pp,pb),
(date('2021-10-30'),bj,aa,ts,sk,sh);

(8, 'Batosai23', 'Batosai Ednalan'),
(9, 'caite', 'Caite Ednalan'),
(11, 'NarutoUzumaki', 'Naruto Uzumaki'),
(12, 'SasukeUchiha', 'Sasuke Uchiha');

ALTER TABLE `users`
  ADD PRIMARY KEY (`date`);

