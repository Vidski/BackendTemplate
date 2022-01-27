manageHomePage();
removeElements();
addEyeToSeeProfile();
changeHeaders();

function manageHomePage(){
  moveToHome();
  checkLogOut();
  addHomeButton();
}

function checkLogOut() {
  if (window.location.pathname == '/admin/logout/') {
    localStorage.clear();
  }
}

function moveToHome() {
  var firstTime = localStorage.getItem('firstTime');
  if (firstTime == null) {
    localStorage.setItem('firstTime', true);
  }
  if (window.location.pathname === '/admin/' && firstTime == 'true') {
    localStorage.setItem('firstTime', false);
    window.location.href = '/home/admin/';
  }
}

function addHomeButton() {
  const navbar = $('.nav.nav-pills.nav-sidebar'+
  '.flex-column.nav-flat.nav-compact');
  navbar.prepend('<li class="nav-item">' +
  '<a href="/home/admin/" class="nav-link">' +
  '<i class="nav-icon fas fa-home">' +
  '</i>' +
  '<p>Home</p>' +
  '</a></li>');
  $('#home-button').click(function () {
    window.location.href = '/admin/';
  });
}

function removeElements() {
  const profileButton = $('.user-panel.mt-3.pb-3.mb-3.d-flex');
  profileButton.remove();
  const logTime = $('.logs-time');
  logTime.remove();
  const changeButton = $('.btn.btn-sm.btn-outline-info.btn-flat.changelink');
  changeButton.remove();
}

function changeHeaders() {
  $search_form = $('#changelist-search');
  if ($search_form.length > 0) {
    $header = $('.card-header .card-title');
    $content = $('.card-tools.form-inline');
    customizeHeader($header);
    hideContent($content);
    manageToggle($header, $content);
  }
}

function addEyeToSeeProfile(){
  $('.dropdown-item.dropdown-footer').prepend('<i class="fas fa-eye"></i>');
}

function customizeHeader(header){
  header.append('<i class="fas fa-chevron-right rotate"></i>');
  header.css('cursor', 'pointer');
}

function hideContent(content) {
  content.toggle(15);
}

function manageToggle(header, content) {
  header.click(function () {
    $icon = $('.fas.fa-chevron-right.rotate');
    $icon.toggleClass("down");
    content.slideToggle(500);
  });
}
