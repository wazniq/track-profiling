;Autolisp Programme for plotting  levels
;Athour--N.Aravindan

(defun c:profile ()
(setvar "cmdecho" 0)
(setvar "blipmode" 0)
;(setq scx 10.0)
;(setq scy 150)
(setq scx (getreal "\n\n Enter Horiz Scale factor <default 1Stn = 10 mm>:"))
(if (= scx nil ) (setq scx 10.0) )
(setq sy (getreal "\n\n Enter Vert Scale factor <default 10 mm = 1 mm>:"))
(if (= sy nil ) (setq sy 1.5))
(setq scy (* sy 100))

(setq ep 0)
(while ( < ep 2 )
;;(setq ep (getint "\n\n Enter 0  for  Exist. Level  1 for Prop. Level :"))
;;(if (= ep nil ) (setq ep 1) )
;;(if (= ep 1)
;;(progn
(setq lyrno 1)
(setq lyrno (getint "\n\n Enter Layer No :"))
(command "layer" "m" lyrno "")
(command "layer" "c" lyrno lyrno "")
;;):--progn
;;);--if
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
 (command "zoom"  "w"  "-100,-100" 
	(list (* (- stnt stnf) scx) (* (- MAXPRL MINPRL) scy)))
(if (= ep 0)
(progn 
(setq hix (+(* (- stnt stnf) scx) 200) )
(setq hiy (+(* (- MAXPRL MINPRL) scy) 100) )         	
(setq lox -100)
(setq loy -100)
(command "line" "-100,-100" (list lox hiy ) (list hix hiy) (list hix loy) "c")
(command "text" (list (/( - hix lox ) 4)   (- hiy 100 ))   20  0 "VERTICAL PROFILE")
);---of progn
);---of if 
 (setq lev  (open  "levels.txt"  "r"))
 (setq trec (read-line lev))
 (if trec 
	(progn 
          (if (= ep 0)
	 (progn
	 (setq sp (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 5 8)) minerl) scy))
	 );--of setq
	 (setq stntxt (substr trec 1 4))
         (setq txtwrt (substr trec 5 8))
         (command "text" (list ( - (car sp) 60) -110 ) 5.0 0 "STN No.")
	 (command "text" (list ( - (car sp) 60) -80  ) 5.0 0 "Exist. RL.")
	 (command "text" (list (car sp) -120 ) 5.0 90 stntxt)
         (command "text" (list (car sp) -100 ) 5.0 90 txtwrt)
	 );--of progn
         (progn
	 (setq 	sp (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 13 8)) minerl) scy))
	 );--of setq
(setq txtwrt (substr trec 13 8))
(setq diftxt (substr trec 21 4))
(command "text" (list ( - (car sp) 60) -40  ) 5.0 0 "Prop. RL.")
(command "text" (list ( - (car sp) 60) -15  ) 5.0 0 "Level Diff")
(command "text" (list (car sp) -60  ) 5.0 90 txtwrt)
(command "text" (list (car sp) -25  ) 5.0 90 diftxt)
	 );--of progn
	 ) :--of if ep
	);--of progn 
 );---of if trec
 (while trec
	(setq trec (read-line lev))
	(if trec
	 (progn
          (if (= ep 0)
          (progn
	  (setq sp1 (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 5 8)) minerl) scy))
	 );--of setq
         (setq stntxt (substr trec 1 4))
         (setq txtwrt (substr trec 5 8))
         );-of progn
(progn
	(setq	sp1 (list (* (- (atoi (substr trec 1 4)) stnf) scx) 
			(* (- (atof (substr trec 13 8)) minerl) scy))
	  );--of setq
(setq txtwrt (substr trec 13 8))
(setq diftxt (substr trec 21 4))
);-of progn
         ) :--of if ep

	  (command "line" sp sp1 "")
	  (setq sp sp1 );---sp2 sp3)
(if (= ep 0)
(progn
(command "text" (list (car sp) -120 ) 5.0 90 stntxt)
(command "text" (list (car sp) -100 ) 5.0 90 txtwrt)
);-of progn
(progn
(command "text" (list (car sp) -60  ) 5.0 90 txtwrt)
(command "text" (list (car sp) -25  ) 5.0 90 diftxt)
);-of progn
);-of if
	 );--of progn		
	);--of if
 );--of while
 );--of progn
);--of if lrec  
(setq ep (+ ep 1))
);-of while
(command "zoom" "e")
(setvar "blipmode" 1)        
(setvar "cmdecho" 1)
);--of defun
