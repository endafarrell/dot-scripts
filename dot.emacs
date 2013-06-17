(require 'epa-file)  (epa-file-enable)

;; This gets my cascalog setup going
(add-to-list 'load-path (expand-file-name "~/.cascalog/emacs"))
(load "dot-cascalog-autoloads")
(dolist (feature '(dot-cascalog-paredit dot-cascalog-nrepl dot-cascalog-emacs dot-cascalog-clojure dot-cascalog-elpa dot-cascalog-ac))
  (require feature))

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-names-vector ["#2e3436" "#a40000" "#4e9a06" "#c4a000" "#204a87" "#5c3566" "#729fcf" "#eeeeec"])
 '(canlock-password "b2a08438282c9b31c399190ef79a6f5e1b54831b")
 '(custom-enabled-themes (quote (tango-dark)))
 '(gud-gdb-command-name "gdb --annotate=1")
 '(large-file-warning-threshold nil)
 '(safe-local-variable-values (quote ((nxml-child-indent . 4)))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
;; ORG MODE customisation
;; The following lines are always needed. Choose your own keys.
(add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))
(add-hook 'org-mode-hook 'turn-on-font-lock) ; not needed when global-font-lock-mode is on
(global-set-key "\C-cl" 'org-store-link)
(global-set-key "\C-ca" 'org-agenda)
(global-set-key "\C-cb" 'org-iswitchb)
(setq org-startup-indented 't)

;; 
(add-hook 'text-mode-hook 'turn-on-auto-fill)
(add-hook 'text-mode-hook '(lambda() (set-fill-column 70)))

;;
(tool-bar-mode 0)
(menu-bar-mode 0)
(server-start)

;; http://stackoverflow.com/questions/1231188/emacs-list-buffers-behavior
(global-set-key "\C-x\C-b" 'buffer-menu)

