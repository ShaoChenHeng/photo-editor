;;; Installation:
;;
;; Put eaf-photo-editor.el to your load-path.
;; The load-path is usually ~/elisp/.
;; It's set in your ~/.emacs like this:
;; (add-to-list 'load-path (expand-file-name "~/elisp"))
;;
;; And the following to your ~/.emacs startup file.
;;
;; (require 'eaf-photo-editor)
;;
;; No need more.

;;; Customize:
;;
;;
;;
;; All of the above can customize by:
;;      M-x customize-group RET eaf-vue-demo RET
;;

;;; TODO
;;
;;
;;

;;; Require


;;; Code:

;;;###autoload
(defun eaf-open-photo-editor ()
  "Open EAF vue demo"
  (interactive)
  (eaf-open "eaf-photo-editor" "photo-editor"))

(defcustom eaf-vue-demo-keybinding
  '(("<f12>" . "open_devtools"))
  "The keybinding of EAF Vue demo."
  :type 'cons)

(add-to-list 'eaf-app-binding-alist '("photo-editor" . eaf-vue-demo-keybinding))

(setq eaf-vue-demo-module-path (concat (file-name-directory load-file-name) "buffer.py"))
(add-to-list 'eaf-app-module-path-alist '("photo-editor" . eaf-vue-demo-module-path))

(provide 'eaf-photo-editor)

;;; eaf-photo-editor.el ends here
