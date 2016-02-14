jQuery.noConflict();

jQuery(document).ready(function() {		

	if(jQuery('#campusMap1').length) {
		jQuery('#campusMap1').fancybox({
			'frameWidth':	980,
			'frameHeight':	550
		});
		jQuery('#campusMap2').fancybox({
			'frameWidth':	980,
			'frameHeight':	550
		});
	}
	
	// Frontpage dynamic banner image
	if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i))) {
		return;
	} else {
		if(jQuery('#homepageBanner').length) {
			jQuery('#homepageBanner')
			.cycle({ 
				fx:		'fade', 
				timeout:10000,
				speed:	3000,
				pause: 1,
				pager:	'#homepageBannerPager'
			});
		}
	}
	
	// Image Panel Widgets
	if(jQuery('#imagePanelLarge').length) {
		jQuery('#imagePanelLarge ul')
		.cycle({ 
			fx:		'fade', 
			pause:	1,
			next:   '#nextLarge', 
			prev:   '#prevLarge' 
		});
	}
	if(jQuery('#imagePanelLarge.black').length) {
		jQuery('#imagePanelLarge.black ul')
		.cycle({ 
			fx:		'fade', 
			timeout:10000,
			speed:	3000,
			pause: 	1,
			pager:	'#pager'
		});
	}
	if(jQuery('#imagePanelSmall').length) {
	jQuery('#imagePanelSmall ul')
		.after('<div id="pager">')
		.cycle({ 
			fx:		'fade', 
			pause:	1,
			pager:	'#pager'
		});
	}
	/** 
	 * JUMP MENU
	 */
	// This hides the 'Go' button if JS is enabled and adds in an onChange function
	if(jQuery('#information_form').length) {		
		jQuery('#information_form :submit').remove();
		// This uses the combobox plugin to allow us to style the select element
		jQuery('#goto').change(function() {
			window.location = jQuery(this).val();	
		});
		/* this is the code for the sexy-combo plugin, we've decedid to disable this for now as it's proving a little fragile when the text is resized
		jQuery("#goto").sexyCombo({
			textChangeCallback: function() {
				window.location = this.getHiddenValue();
			}
		});
		*/
	}
	/**
	 * COURSEFINDER VALIDATION
	 *
	 * This hides the submit button on courses if there has been no categories and/or
	 * metadata assigned. This was a common problem once CF went live which resulted
	 * in people not seeing the error message asking for this data
	 */
	 if(jQuery('#coursefinderSubmit').length) {
		$submit = jQuery('#coursefinderSubmit');
		$finish = jQuery('.generic_finish');
		jQuery('.coursefinderForm tr').hover(function() {
			validateCourse();
	   });
	 }
	 function validateCourse() {
		 if( !jQuery('#metadata_description').val() || !jQuery('#categories\\:bespoke').val() || !jQuery('#categories\\:taxonomy').val() ) {
			$submit.attr('disabled','true'); 
			$submit.addClass('button_disabled');
			if(!jQuery('#warning').length) {
				$finish.prepend('<span id="warning">Please ensure this course has categories and metadata before saving</span>');
			}
		} else {
			jQuery('#coursefinderSubmit').removeAttr('disabled');
			$submit.removeClass('button_disabled');
			if(jQuery('#warning').length) {
				jQuery('#warning').remove();
			}
		}
	}
	 
	/**
	 * RESEARCH NEWS WIDGET
	 *
	 * This controls the tabbing of research news
	 */
	if(jQuery('#researchNews').length) {
		jQuery('ul.widget_news_tabs li a').each(function (index, tabElement) {
			jQuery(tabElement).click(function(event) {
				var selectedID = tabElement.id;
				jQuery('ul.widget_news_category').each(function (index, listElement) {
					if (listElement.id + '_tab' == selectedID) {
						jQuery('#' + listElement.id + '_tab').parent().addClass('widget_news_tab_active');
						jQuery(listElement).show();
					} else {
						jQuery('#' + listElement.id + '_tab').parent().removeClass('widget_news_tab_active');
						jQuery(listElement).hide();
					}
				});			
				// Stop the browser from following the link
				return false;
			});
		});
	}
	
	if(jQuery('#researchNews2').length) {
	jQuery('#researchTabs li').each(function(j,val) {
		
		/* Convert spaces to non-breaking spaces so that the text doesn't wrap */
		jQuery('a',this).html(jQuery('a',this).html().replace(/ /g,'&nbsp;'));
		
		/* calculate tab widths in collapsed and expanded states */
		var curWidth = jQuery(this).css('width');
		jQuery(this).css({'width':'auto'});
		var newWidth = jQuery(this).innerWidth();
		jQuery(this).css({'width':curWidth});
		
		/* Split the tab label and wrap a class around the first word
			This allows us to hide the rest and not end up with "HEALTH A" for eg */
		var split = jQuery('a',this).html().split('&nbsp;');
		if(split.length > 1) {
			var label = split[0] + '<span class="labelHidden">';
			var i=1;
			while (i < split.length) {
				label = label + '&nbsp;' + split[i];
				i++;
			}
			label = label + '</span>';
		}
		jQuery('a',this).html(label);
		
		/* add the hover animation to any tabs where the expanded width is larger
			than the collapsed state (this prevents any unneccessary scaling) */
		if(newWidth>curWidth.replace('px','')) {
			jQuery(this).hover(
				function () {
					
					jQuery('span',this).removeClass('labelHidden');
					jQuery(this).animate({
						width:newWidth
						}, 100 );
					}, 
				function () {
					jQuery('span',this).addClass('labelHidden');	
					jQuery(this).animate({
						width:curWidth
					}, 100
					);			
				}
			);
		}
		
		jQuery(this).click(function() {
			jQuery('.researchArticles').css('visibility','hidden');
			jQuery('#researchTabs li').removeClass('selected');
			jQuery(this).addClass('selected');
			jQuery('#pane'+j+' li').fadeOut(1,function() {
				jQuery('#pane'+j).css({'z-index':'1','visibility':'visible'});
				jQuery('#pane'+j+' li').fadeIn('fast');
				}
			);
			return false;
		});
		
	});
	};

});