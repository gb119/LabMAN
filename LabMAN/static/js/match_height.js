    	function matchHeights() {
		//code to run when document loads
		var lh,rh,lp,rp,th;
		lh=$("#treenavlist").height();
		rh=$("#content").height();
		th=(lh>rh?lh:rh);
		lp=th-lh+16;
		rp=th-rh;
		$("#leftcol-pad").height(lp);
		$("#rightcol-pad").height(rp);
	};
// JavaScript Document