(function(){
  function post(url){
    return fetch(url, {method:'POST', headers: {'X-CSRFToken': window.csrfToken}}).then(r=>r.json());
  }
  document.addEventListener('click', function(e){
    const btn = e.target.closest('button[data-action]');
    if(!btn) return;
    const id = btn.getAttribute('data-id');
    const action = btn.getAttribute('data-action');
    if(!id || !action) return;
    const url = action==='like' ? `/quote/${id}/like/` : `/quote/${id}/dislike/`;
    btn.disabled = true;
    post(url).then(data=>{
      const root = btn.closest('.card');
      if(!root) return;
      const likeEl = root.querySelector('.count-like');
      const dislikeEl = root.querySelector('.count-dislike');
      if(likeEl && typeof data.likes !== 'undefined') likeEl.textContent = data.likes;
      if(dislikeEl && typeof data.dislikes !== 'undefined') dislikeEl.textContent = data.dislikes;
      setTimeout(()=>{ btn.disabled = false; }, 350);
    }).catch(()=>{ btn.disabled = false; });
  });
})();
