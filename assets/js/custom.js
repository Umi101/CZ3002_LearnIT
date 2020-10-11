// likes
$('#question-like').click(function() {
  let questionId = $(this).data('question');
  let url = 'questions/' + questionId + '/like-or-dislike';
  let likesCounterDiv = $('#question-likes-counter');

  let _this = $(this)

  $.get( url, function( response ) {
    let message = response.message;

    switchIcons(_this, message);
    incrementOrDecrementLikes(likesCounterDiv, message);
  });
})

$('.reply-like').click(function() {
  let replyId = $(this).data('reply');
  let url = 'replies/' + replyId + '/like-or-dislike';
  let likesCounterDiv = $('#reply-likes-counter-' + replyId);

  let _this = $(this)

  $.get( url, function( response ) {
    let message = response.message;

    switchIcons(_this, message);
    incrementOrDecrementLikes(likesCounterDiv, message);
  });
})

function switchIcons(element, message) {
  if(message === 'liked') {
    element.attr('src','/static/images/dislike.svg');
  } else {
    element.attr('src','/static/images/like.svg');
  }
}

function decrementLikes(element) {
  let currentNumOfLikes = parseInt(element.html());
  let newHtml;

  if (currentNumOfLikes !== 0) {
    currentNumOfLikes -= 1;
    if (currentNumOfLikes === 1) {
      newHtml = currentNumOfLikes + ' like'
    } else {
      newHtml = currentNumOfLikes + ' likes'
    }
  }element

  element.html(newHtml);
}

function incrementLikes(element) {
  let currentNumOfLikes = parseInt(element.html());
  let newHtml;

  currentNumOfLikes += 1;
  if (currentNumOfLikes === 1) {
    newHtml = currentNumOfLikes + ' like'
  } else {
    newHtml = currentNumOfLikes + ' likes'
  }

  element.html(newHtml);
}

function incrementOrDecrementLikes(element, message) {
  if (message === 'liked') {
    incrementLikes(element);
  } else {
    decrementLikes(element);
  }
}

// mark question as solved from detail view
$('#solved').click(function(event) {
  event.preventDefault();
  console.log('clicked')

  let url = $(this).attr('href');

  let _this = $(this)

  $.get( url, function( response ) {
    let message = response.message;

    if (message === 'solved') {
      $(_this).text("SOLVED");
    } 
   
  });
})