tinymce.init({
  selector: 'textarea',
  height: 250,
  theme: 'modern',
  plugins: [
    'advlist autolink lists link image charmap print preview hr anchor pagebreak',
    'searchreplace wordcount visualblocks visualchars code fullscreen',
    'insertdatetime media nonbreaking save table contextmenu directionality',
    'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'
  ],
  textpattern_patterns: [
     {start: '*', end: '*', format: 'italic'},
     {start: '**', end: '**', format: 'bold'},
     {start: '#', format: 'h1'},
     {start: '##', format: 'h2'},
     {start: '###', format: 'h3'},
     {start: '####', format: 'h4'},
     {start: '#####', format: 'h5'},
     {start: '######', format: 'h6'},
     {start: '1. ', cmd: 'InsertOrderedList'},
     {start: '* ', cmd: 'InsertUnorderedList'},
     {start: '- ', cmd: 'InsertUnorderedList'}
  ],
  toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
  toolbar2: 'print preview media | forecolor backcolor emoticons | codesample',
  image_advtab: true,
  visualblocks_default_state: true,
  theme_advanced_toolbar_location : "top",
  theme_advanced_toolbar_align : "left",
 });
