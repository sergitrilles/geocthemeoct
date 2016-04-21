this.ckan.module('blog-admin', function (jQuery) {
  return {
    initialize: function () {
      jQuery('.remove-link').click(function () {
        console.log('Hej');
      });
    }
  };
});
