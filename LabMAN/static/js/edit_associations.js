function reg_files_handlers() {
	$("#new_assoc").click(new_assoc);
	$(".editable").click(load_edit_box);

}

function load_edit_box(event) {
	alert($(this).attr("id"));
}

function new_assoc(event){
	event.preventDefault();
	var basedir=$("input#basedir").val();
	var id=$("input#id").val();
	var url=basedir+"/ajax/files_assoc.php?page=add&file="+id;
	$.get(url,
		function(data) {
			$("#associations").append(data);
			var row=$('.assoc_row:last').attr('id');
			$('#'+row+'> td:eq(0) > select').change(
				function () { 
					switch_assoc(row);
				}
			);
			$('#'+row+'> td:eq(2) > img.edit-apply').click(
				function () {
					apply_assoc(row);
				}
			);
			$('#'+row+'> td:eq(2) > img.edit-remove').click(
				function () {
					$('#'+row).remove();
				}
			);
		}
	);
    return false;
}

function switch_assoc(row) {
	var basedir=$("input#basedir").val();
	var id=$("input#id").val();
	var what=$('tr#'+row+' > td:eq(0) > select').val();
	var url=basedir+'/ajax/interface.php?what='+what;
	$('tr#'+row+' > td:eq(1)').load(url);
}

function apply_assoc(row) {
	var basedir=$("input#basedir").val();
	var id=$("input#id").val();
	var what=$('tr#'+row+' > td:eq(0) > select').val();
	var target=$('tr#'+row+' > td:eq(1) > select').val();
	var url=basedir+'/ajax/files_assoc.php?page=apply&what='+what+'&target='+target+'&id='+id;
	$('tr#'+row).load(url);
}
