(setq gnus-select-method
       '(nntp "cutlass"
	  (nntp-address "nntp.cutlass.nokia.com")
	  (nntp-open-connection-function nntp-open-ssl-stream)
	  (nntp-port-number 563)
	  (nntp-authinfo-file "~/.authinfo.gpg")))

(setq user-mail-address "enda.farrell@nokia.com")
(setq user-full-name "Enda Farrell")

;; from http://www.emacswiki.org/emacs/GnusFormatting
(setq-default
     gnus-summary-line-format "%U%R%z %d | %-20,20n | %-4,4N | %B%s\n"
     gnus-summary-thread-gathering-function 'gnus-gather-threads-by-references
     gnus-thread-sort-functions '(gnus-thread-sort-by-date))

;; No HTML mail
(setq mm-discouraged-alternatives '("text/html" "text/richtext"))

;; There is a warning about messages having lines longer than
;; 79 chars that I would like to avoid
;; this didn't work (setq default-fill-column 72)
;; remember that M-q will reformat before you post if you want!
(unless (boundp 'message-fill-column)
   (add-hook 'message-mode-hook
	 (lambda ()
	   (setq fill-column 72)
	   (turn-on-auto-fill))))

;; It is nice to have GNUS auto-refresh
(gnus-demon-add-handler 'gnus-demon-scan-news 5 1)
(gnus-demon-add-handler 'gnus-demon-scan-timestamps nil 30)
(gnus-demon-init)

;; Let the Mac OSX /usr/bin/open figure out what to do with
;; these pdf files 
(setq gnus-uu-user-view-rules
      (list '("\\.\(doc\|xsl\|pdf\|png\|jpg\)$" "/usr/bin/open %s")))

;; Loading only unread messages can be annoying if you have
;; threaded view enabled,
(setq gnus-fetch-old-headers 'some)

;; Make Gnus into an offline newsreader.
(setq gnus-agent t) ; Now the default.

;; 3.11 Asynchronous Article Fetching
(setq gnus-asynchronous t)
(setq gnus-use-article-prefetch t)
;; 3.12 Article Caching
(setq gnus-use-cache t)
(setq gnus-use-long-file-name t)

;; send mail
(setq starttls-use-gnutls t
      starttls-gnutls-program "gnutls-cli"
      starttls-extra-arguments nil
      smtpmail-smtp-server "smtp.nokia.com"
      smtpmail-default-smtp-server "smtp.nokia.com"
      smtpmail-local-domain "nokia.com"
      send-mail-function 'smtpmail-send-it
      message-send-mail-function 'smtpmail-send-it
      smtpmail-smtp-service 25)
