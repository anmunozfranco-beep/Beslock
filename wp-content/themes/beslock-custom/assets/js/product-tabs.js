/* Accessible tabs for product page (mobile-first)
 * - toggles two panels: Especificaciones / Reviews
 * - supports click and keyboard (ArrowLeft/ArrowRight/Home/End)
 */
(function(){
  'use strict';

  function initTabs(context){
    var root = context || document;
    var blocks = root.querySelectorAll('.product-tabs');
    if(!blocks || blocks.length===0) return;
    blocks.forEach(function(block){
      var tabs = Array.prototype.slice.call(block.querySelectorAll('[role="tab"]'));
      var panels = Array.prototype.slice.call(block.querySelectorAll('[role="tabpanel"]'));

      function activateTab(tab, focusPanel){
        tabs.forEach(function(t){
          var selected = t === tab;
          t.classList.toggle('product-tabs__tab--active', selected);
          t.setAttribute('aria-selected', selected ? 'true' : 'false');
        });
        panels.forEach(function(p){
          var show = p.id === tab.getAttribute('aria-controls');
          if(show){
            p.removeAttribute('hidden');
            p.setAttribute('tabindex','0');
          } else {
            p.setAttribute('hidden','');
            p.removeAttribute('tabindex');
          }
        });
        // move focus into panel for keyboard users when requested by caller
        try{
          if (focusPanel) {
            var panel = document.getElementById(tab.getAttribute('aria-controls'));
            if(panel) panel.focus();
          }
        }catch(e){}
      }

      tabs.forEach(function(tab, idx){
        tab.addEventListener('click', function(e){ e.preventDefault(); activateTab(tab); });
        tab.addEventListener('keydown', function(e){
          var key = e.key || e.keyCode;
          if(key === 'ArrowRight' || key === 'Right' || key === 39){ e.preventDefault(); var next = tabs[(idx+1)%tabs.length]; next.focus(); activateTab(next, true); }
          if(key === 'ArrowLeft' || key === 'Left' || key === 37){ e.preventDefault(); var prev = tabs[(idx-1+tabs.length)%tabs.length]; prev.focus(); activateTab(prev, true); }
          if(key === 'Home' || key === 'Home' || key === 36){ e.preventDefault(); tabs[0].focus(); activateTab(tabs[0], true); }
          if(key === 'End' || key === 'End' || key === 35){ e.preventDefault(); tabs[tabs.length-1].focus(); activateTab(tabs[tabs.length-1], true); }
        });
      });

      // ensure initial state
      var active = block.querySelector('[role="tab"][aria-selected="true"]') || tabs[0];
      if(active) activateTab(active, false);
    });
  }

  function openReplyDialog(dialog, trigger){
    if(!dialog) return;

    dialog.__beslockTrigger = trigger || dialog.__beslockTrigger || null;

    if(typeof dialog.showModal === 'function'){
      if(!dialog.open) dialog.showModal();
    } else {
      dialog.setAttribute('open', 'open');
    }

    if(dialog.__beslockTrigger){
      dialog.__beslockTrigger.setAttribute('aria-expanded', 'true');
    }

    var firstField = dialog.querySelector('textarea, input:not([type="hidden"]), button');
    if(firstField){
      try{ firstField.focus(); }catch(e){}
    }
  }

  function closeReplyDialog(dialog){
    if(!dialog) return;

    if(typeof dialog.close === 'function' && dialog.open){
      dialog.close();
    } else {
      dialog.removeAttribute('open');
    }

    dialog.removeAttribute('data-open-on-load');

    if(dialog.__beslockTrigger){
      dialog.__beslockTrigger.setAttribute('aria-expanded', 'false');
      try{ dialog.__beslockTrigger.focus(); }catch(e){}
    }
  }

  function initReplyDialogs(context){
    var root = context || document;
    var triggers = root.querySelectorAll('[data-reply-dialog-trigger]');
    var dialogs = root.querySelectorAll('.product-interactions__reply-dialog');

    dialogs.forEach(function(dialog){
      if(dialog.dataset.replyDialogBound === 'true') return;

      dialog.dataset.replyDialogBound = 'true';

      var closeButtons = dialog.querySelectorAll('[data-reply-dialog-close]');
      closeButtons.forEach(function(button){
        button.addEventListener('click', function(){
          closeReplyDialog(dialog);
        });
      });

      dialog.addEventListener('cancel', function(event){
        event.preventDefault();
        closeReplyDialog(dialog);
      });

      dialog.addEventListener('click', function(event){
        if(event.target === dialog){
          closeReplyDialog(dialog);
        }
      });
    });

    triggers.forEach(function(trigger){
      if(trigger.dataset.replyDialogBound === 'true') return;

      trigger.dataset.replyDialogBound = 'true';
      trigger.setAttribute('aria-expanded', trigger.getAttribute('aria-expanded') || 'false');

      trigger.addEventListener('click', function(){
        var dialogId = trigger.getAttribute('data-reply-dialog-id');
        if(!dialogId) return;

        var dialog = document.getElementById(dialogId);
        openReplyDialog(dialog, trigger);
      });
    });

    dialogs.forEach(function(dialog){
      if(dialog.getAttribute('data-open-on-load') === 'true'){
        var trigger = document.querySelector('[data-reply-dialog-id="' + dialog.id + '"]');
        openReplyDialog(dialog, trigger);
      }
    });
  }

  function init(context){
    initTabs(context);
    initReplyDialogs(context);
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ init(document); }); else init(document);
  // expose for partial re-initialization
  window.__beslock_product_tabs_init = init;
})();
