% for picid in sorted(pics, key=lambda key: -pics[key]["time_added"]):
% 	pic = pics[picid]
<div class="col-lg-3 col-md-4 col-xs-6 thumb">
	<div class="thumbnail">
		<a class="thumbnail" href="#">
			<img class="img-responsive" src="/pic/thumb/{{picid}}" style="height:200px; object-fit:cover" alt="">
		</a>
		Cuddles:{{pic["votes"]}}
		<button type="button" onclick="vote('{{picid}}','up')" class="btn btn-default btn-xs">
			<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span>
		</button>
		<button type="button" onclick="vote('{{picid}}','down')" class="btn btn-default btn-xs">
			<span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
		</button>
	</div>		
</div>
% end