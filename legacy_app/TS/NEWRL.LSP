;lisp for plotting one  rail level

;(defun  wrtxt (just pt ht ang txt /oldlyr oldclr)
;	(setq oldlyr (getvar "CLAYER") oldclr (getvar "CECOLOR"))
;	(command "layer" "make"  "text" "")
;	(command "color" 7)
;	(if just (command "text" just pt ht ang txt)
;		 (command "text" pt ht ang txt)
;	)
;	(command "color" (substr oldclr 1 1))
;	(command "layer" "set" oldlyr "")
;)



(defun c:profile ()
(setvar "cmdecho" 0)
(setvar "blipmode" 0)

;(setq scx (getreal "\n\n Enter Horiz Scale factor <default 1Stn = 10 mm>:"))
;(if (= scx nil ) (setq scx 10.0) )
;(setq sy (getreal "\n\n Enter Vert Scale factor <default 10 mm = 1 mm>:"))
;(if (= sy nil ) (setq sy 100))
;(setq scy (* sy 100))

(setq scx 10.0)
(setq scy 150)
(setq ep (getint "\n\n Enter 0  for  ERL 1 for PRL:"))
(if (= ep nil ) (setq ep 1) )
(if (= ep 1)
(progn
(setq lyrno (getint "\n\n Enter Layer No :"))
(command "layer" "m" lyrno "")
(command "layer" "c" lyrno lyrno "")

):--progn
);--if
(setq frc (open "SDATA.TXT"  "r" ))
(setq lrec (read-line frc))
(if lrec
 (progn
  (setq TNO  (atoi (substr lrec 1 2))
		CORR (substr lrec 3 1)
                STNF (atoi (substr lrec 4 4))
                STNT (atoi (substr lrec 8 4)) 
                MAXERL (atof (substr lrec 12 8))
                MINERL (atof (substr lrec 20 8))
                MAXPRL (atof (substr lrec 28 8))
                MINPRL (atof (substr lrec 36 8)))
 (command "limits"  "off")
 (command "zoom"  "w"  "-200,-200" 
	(list (* (- stnt stnf) scx) (* (- MAXPRL MINPRL) scy)))
 ;(setq bp -200 txtht 2.0)
 (setq lev  (open  "levels.txt"  "r"))
 (setq trec (read-line lev))
 (if trec 
	(progn 
          (if (= ep 0)
	 (setq sp (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 5 8)) minerl) scy))
	 );--of setq

	(setq 	sp (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 13 8)) minerl) scy))
	 );--of setq
         ) :--of if ep

 ;(command "text" (list (100) (*(lyrno 50))) 3.0 0 (itoa(lyrno)))

	);--of progn 
 );---of if trec
 (while trec
	(setq trec (read-line lev))
	(if trec
	 (progn
          (if (= ep 0)

	  (setq sp1 (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 5 8)) minerl) scy))
	 );--of setq

	(setq	sp1 (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 13 8)) minerl) scy))
	  );--of setq
         ) :--of if ep

	  (command "line" sp sp1 "")
;	  (command "line" sp2 sp3 "")
	  (setq sp sp1 );---sp2 sp3)
;	(wrtxt nil (list (car(sp)) (bp)) txtht 90 trec)
;(command "text" (list (car sp) -70 ) 5.0 90 trec)
	 );--of progn		
	);--of if
 );--of while
 );--of progn
);--of if lrec  
(command "zoom" "e")
(setvar "blipmode" 1)        
(setvar "cmdecho" 1)
);--of defun
