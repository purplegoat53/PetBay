<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
		<script src="/static/js/sjcl.js"></script>
	<script src="/static/js/login.js"></script>
	<script src="/static/js/vote.js"></script>


    <title>PetBay</title>

    <!-- Bootstrap Core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="/static/css/thumbnail-gallery.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <!-- Navigation -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
			<a class="navbar-brand" rel="home" href="/" title="PetBay">
				<img style="max-width:75px; margin-top: -7px;"
				 src="/static/css/aww/logotranssmall.png">
			</a>
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Front</a>
            </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li>
                        <a href="/halloffame">Hall of Fame</a>
                    </li>
                    <li>
                        <a href="/profile">Profile</a>
                    </li>
					<li>
						<a data-toggle="modal" href="#regModal" data-backdrop="true" >Register</a>
					</li>
                </ul>
				<!--http://bootsnipp.com/snippets/featured/horizontal-login-form-in-navbar-with-prepend-->
				% if email is None:
				<form id="signin" class="navbar-form navbar-right" role="form">
					<div class="input-group">
						<span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
						<input id="email" type="email" class="form-control" name="email" value="" placeholder="Email Address">                                        
					</div>

					<div class="input-group">
						<span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
						<input id="password" type="password" class="form-control" name="password" value="" placeholder="Password">                                        
					</div>

					<button type="submit" onclick="login1(event)" class="btn btn-primary">Login</button>
				</form>
				% else:
				{{email}}
				% end
				
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->	
    </nav>
	
	<!--http://bootsnipp.com/snippets/8VmZ-->
	<div id="regModal" class="modal fade" role="dialog" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-dialog" aria-labelledby="myModalLabel" aria-hidden="true">
			<div class="modal-content">
				<div class="modal-header">
					<legend> 
						<img style="max-width:75px; margin-top: -7px;"src="/static/css/aww/logo.png">&nbsp;&nbsp;&nbsp;Sign up!
					</legend>
				</div>
				<div id="entry_fields" class="modal-body">
					<form id="regForm" class="form" role="form">
						<input id="newEmail" class="form-control" name="email" placeholder="Your Email" type="email" />
						<input id="reNewEmail" class="form-control" name="reenteremail" placeholder="Re-enter Email" type="email" />
						<input id="newPass" class="form-control" name="password" placeholder="New Password" type="password" />
						<input id="reNewPass" class="form-control" name="reenterpassword" placeholder="Re-enter Password" type="password" />

						<button class="btn btn-lg btn-primary btn-block" onclick="register(event)" type="submit">Sign up</button>	
					</form>
				</div>
			</div>
		</div>
	</div>

    <!-- Page Content -->
    <div class="container">

        <div class="row">

            <div class="col-lg-12">
				<div class="input-group" style="float:right; margin-top:30px">
					<label class="control-label">Select File</label>
					<input id="input-1" type="file" class="file">
				</div>	
                <h1 class="page-header">Latest cuddles</h1>					
            </div>
			<!--<div class="col-xs-12 col-sm-12 col-md-4 well well-sm">
				<legend><a href="#"><i class="glyphicon glyphicon-globe"></i></a> Sign up!</legend>
				<form action="#" method="post" class="form" role="form">
				<div class="row">
					<div class="col-xs-6 col-md-6">
						<input class="form-control" name="firstname" placeholder="First Name" type="text"
							required autofocus />
					</div>
					<div class="col-xs-6 col-md-6">
						<input class="form-control" name="lastname" placeholder="Last Name" type="text" required />
					</div>
				</div>
				<input class="form-control" name="youremail" placeholder="Your Email" type="email" />
				<input class="form-control" name="reenteremail" placeholder="Re-enter Email" type="email" />
				<input class="form-control" name="password" placeholder="New Password" type="password" />
			   
				<br />
				<br />
				<button class="btn btn-lg btn-primary btn-block" type="submit">
					Sign up</button>
				</form>
			</div>-->
			% for picid in pics:
			% 	pic = pics[picid]
            <div class="col-lg-3 col-md-4 col-xs-6 thumb">
				<div class="thumbnail">
					<a class="thumbnail" href="#">
						<img class="img-responsive" src="/pic/thumb/{{picid}}" style="height:200px; object-fit:cover" alt="">
					</a>
					Cuddles:{{pic["votes"]}}
					<button type="button" onclick="upvote('{{picid}}')" class="btn btn-default btn-xs">
						<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span>
					</button>
					<button type="button" class="btn btn-default btn-xs">
						<span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
					</button>
                </div>		
            </div>
			% end
        </div>
		
		<ul class="pagination pagination-sm">
		  <li><a href="?page=1">1</a></li>
		  <li><a href="?page=2">2</a></li>
		  <li><a href="?page=3">3</a></li>
		  <li><a href="?page=4">4</a></li>
		  <li><a href="?page=5">5</a></li>
		</ul>
		
        <hr>

        <!-- Footer -->
        <footer>
            <div class="row">
                <div class="col-lg-12">
                    <p>Copyright &copy; Cuddles inc. 2015</p>
                </div>
            </div>
        </footer>

    </div>
    <!-- /.container -->

    <!-- jQuery -->
    <script src="/static/js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="/static/js/bootstrap.min.js"></script>

</body>

</html>
