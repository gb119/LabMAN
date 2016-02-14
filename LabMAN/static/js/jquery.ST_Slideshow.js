/**
 * ST_Slideshow - JSON based slideshow with jQuery
 *   http://www.stefanhayden.com/slideshow/
 *
 * Licence: GPL 3.0 http://www.opensource.org/licenses/gpl-3.0.html
 *
 * Built on the jQuery library
 *   http://jquery.com
 *
 * Inspired by the "s3slider"
 *   http://www.serie3.info/s3slider/
 */

(function($){  

    $.fn.ST_Slideshow = function(vars) {
        
        var slideArray              = (vars.slideArray != undefined) ? vars.slideArray : console.log('You must set a slideArray to show slides.');
        var element                 = this;
        var timeOut                 = (vars.timeOut != undefined) ? vars.timeOut : 7000;
        var pause                   = false;
        var prev_next               = (vars.prev_next != undefined) ? vars.prev_next : true;
        var play_pause              = (vars.play_pause != undefined) ? vars.play_pause : true;
        var pagination              = (vars.pagination != undefined) ? vars.pagination : true;
        var SlideFade               = (vars.SlideFade != undefined) ? vars.SlideFade : "slow";
        var width	               = (vars.width != undefined) ? vars.width : "200px";
        var CaptionAnimate          = (vars.CaptionAnimate != undefined) ? vars.CaptionAnimate : "slow";
        var CaptionAnimateDelay     = (vars.CaptionAnimateDelay != undefined) ? vars.CaptionAnimateDelay : 500;
        var current                 = null;
        var timeOutFn               = null;
        var wrapper                 = jQuery("#" + element[0].id);
        
        //set up structure
        for(var i=1; i<slideArray.length; i++) {
            wrapper
                .append('<li class="slide"></li>\n')
                .find('li:last')
                .append('<a href="'+ slideArray[i]['link'] +'"><img src="" alt="'+ slideArray[i]['caption'] +'" width="'+width+'" /></a>\n')
                .append('<span></span>\n');
            if(slideArray[i]['caption'] || slideArray[i]['subcaption']) {
                wrapper.find('li.slide:last span')
                    .append('\n<div class="caption">'+ slideArray[i]['caption'] +'</div>\n<div class="subcaption">'+ slideArray[i]['subcaption'] +'</div>\n');        
            } else {
                //the span must exist for the animation to fire correctly.
                wrapper.find('li.slide:last span').css('padding','0px').css('height','0px');
            }
        }//end for
        
        //now that structure is in place grab the elements
        var items       = jQuery("#" + element[0].id + " .slide");
        var itemsSpan   = items.find("span");
        
        //preload 2nd slide
        wrapper.find('li.slide:eq(1) img').attr("src", slideArray[1]['url']);
        wrapper.find('li.slide:eq(1)').addClass("next");
        
        //Set up slideSelect to load. Not needed if JS is not on.
        if(pagination) {
            var slideSelect = "<div class=\"slideSelect\">\n";
            for(var i = 0; i < items.length; i++) {
                slideSelect += "<div>"+(i+1)+"</div>\n";
            }
            if(play_pause) {
                slideSelect += "<span class=\"pause\"></span>\n";
            }
            slideSelect += "</div>\n";
            wrapper.append(slideSelect);
        }
        
        //Set up slideSelect to load. Not needed if JS is not on.
        if(prev_next) {
            var pager = "<div class=\"prev-next\">\n";
            pager += " <span class=\"prev\">Previous</span> |";
            pager += " <span class=\"next\">Next</span>\n";
            pager += " </div>\n";
            wrapper.append(pager);
        }
        
        wrapper.find('div.slideSelect div:eq(0)').addClass("selected");
        wrapper.find('li.slide:eq(0) span').slideDown("slow");
        
        //go to href around image
        items.find('span').click(function(){
            location.href = jQuery(this).parent().find("a").attr('href');
        });//end onClick
        
        //play or pause button
        wrapper.find('div.slideSelect span').click(function(){ 
            if(jQuery(this).hasClass('pause')) { //pause the animation
                $(this).removeClass("pause").addClass("play");
                pause = true;
                window.clearTimeout(timeOutFn);
            } else { //start animation
                $(this).addClass("pause").removeClass("play");
                window.clearTimeout(timeOutFn); //clear timout just to be careful
                pause = false;
                showSlide();
            }
            
        });//end onClick
        
        //go to a specific slide
        wrapper.find('div.slideSelect div').click(function(){
            current = $(this).text()-1; //set this as the next slide to show
            wrapper.find("li.next").removeClass("next"); //remove the slide that was set to show next
            wrapper.find("li:eq("+current+")").addClass("next"); //add this slide as next to show
            window.clearTimeout(timeOutFn);
            showSlide();
        });//end onClick
        
        //go to previous slide
        wrapper.find('div.prev-next .prev').click(function(){
            current = current-2; //-2 because count has already be incrimented to the next slide and you need to fall 2 back
            wrapper.find("li.next").removeClass("next"); //remove the slide that was set to show next
            wrapper.find("li:eq("+current+")").addClass("next"); //add this slide as next to show
            window.clearTimeout(timeOutFn);
            showSlide();
        });//end onClick
        
        //go to next slide
        wrapper.find('div.prev-next .next').click(function(){
            window.clearTimeout(timeOutFn);
            showSlide();
        });
    
        function showSlide() {
            current = (current != null) ? current : 1;
            current = (current == slideArray.length) ? 0 : current; //if you are 1 past the last slide go back to beginning
            
            var thisSlide = wrapper.find('li.slide:eq('+current+')');
            if(thisSlide.find('img').attr("src") == '') { thisSlide.find('img').attr("src", slideArray[current]['url']); }
            
            wrapper.find('li.show span').slideUp(CaptionAnimate, function(){
                $(this).parent().fadeOut(SlideFade, function(){
                        
                    wrapper.find('div.slideSelect .selected').removeClass("selected");
                    wrapper.find('div.slideSelect div:eq('+current+')').addClass("selected");
                    
                    wrapper.find("li.show").removeClass('show');
                    wrapper.find("li.next span")
                        .animate({opacity: 0.7}, CaptionAnimateDelay) //this is a trick to pause a jquery chain
                        .slideDown(CaptionAnimate)
                        .parent()
                        .removeClass("next")
                        .addClass("show");
                        
                    //make sure you are not at end of slides
                    if (current == (slideArray.length-1)) { wrapper.find('li.slide:eq(0)').addClass('next');  } 
                    else { wrapper.find('li.slide:eq('+(current+1)+')').addClass('next');  }
                    
                    current++; //get ready for next slide
                    
                    items.css('display',"block"); //un-fade the slide you fadedOut;
                    if(!pause) {
                        timeOutFn = setTimeout(showSlide, timeOut);
                    }

                });
            });
            
            
        }//end showSlide()
        timeOutFn = setTimeout(showSlide, timeOut);
        
    }//end shermansSlideshow
    
})(jQuery); 