// Remove Chainlit's default stop message while keeping your custom on_stop message
(function () {
  const TARGET_TEXTS = [
    "Task manually stopped.",
  ];

  function isTargetNode(node) {
    if (!node || !node.textContent) return false;
    const txt = node.textContent.trim();
    return TARGET_TEXTS.includes(txt);
  }

  function sweep(root = document) {
    // Try to remove entire message containers if possible
    const all = root.querySelectorAll('*');
    all.forEach((el) => {
      if (isTargetNode(el)) {
        const messageContainer = el.closest('[data-testid="message"], [data-state], article, li, .message, .prose');
        if (messageContainer) {
          messageContainer.remove();
        } else {
          el.remove();
        }
      }
    });
  }

  // Initial sweep after load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => sweep());
  } else {
    sweep();
  }

  // Observe future changes and sweep incrementally
  const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      m.addedNodes && m.addedNodes.forEach((n) => {
        if (n.nodeType === 1) {
          const el = /** @type {Element} */ (n);
          if (isTargetNode(el)) {
            const messageContainer = el.closest('[data-testid="message"], [data-state], article, li, .message, .prose');
            if (messageContainer) {
              messageContainer.remove();
            } else {
              el.remove();
            }
          } else {
            sweep(el);
          }
        }
      });
    }
  });

  observer.observe(document.documentElement || document.body, {
    childList: true,
    subtree: true,
  });
})();
