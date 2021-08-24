let likedNum;

if ($('#likednum')) {
  likedNum = parseInt($('#likednum').text());
}

$('.likebtn').click(async function (e) {
  e.preventDefault();
  const msgId = $(this).parent().attr('class');
  if (this.classList.contains('liked')) {
    $(this).attr('class', 'likebtn btn btn-sm btn-secondary unliked');
    $(this).html('<i class="fa fa-thumbs-up"></i>');
    likedNum--;
    $('#likednum').text(likedNum);
  } else {
    $(this).attr('class', 'likebtn btn btn-sm btn-primary liked');
    $(this).html('<i class="fas fa-star liked"></i>');
    likedNum++;
    $('#likednum').text(likedNum);
  }
  const res = await axios.post(`/users/add_like/${msgId}`);
});

$('.userlikebtn').click(async function (e) {
  e.preventDefault();
  const msgId = $(this).parent().attr('class');
  if (this.classList.contains('liked')) {
    $(this).attr('class', 'likebtn btn btn-sm btn-secondary unliked');
    $(this).html('<i class="fa fa-thumbs-up"></i>');
    this.parentElement.parentElement.remove();
  }
  const res = await axios.post(`/users/add_like/${msgId}`);
});
