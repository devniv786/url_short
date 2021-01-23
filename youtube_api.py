from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Video(name = {name},views = {views},likes = {likes})"

#db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name of the video",required=True)
video_put_args.add_argument("views",type=int,help="Views of the video",required=True)
video_put_args.add_argument("likes",type=int,help="Likes of the video",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Name of the video",required=False)
video_update_args.add_argument("views",type=int,help="Views of the video",required=False)
video_update_args.add_argument("likes",type=int,help="Likes of the video",required=False)

resource_fields = {
    "id":fields.Integer,
    "name":fields.String,
    "views":fields.Integer,
    "likes":fields.Integer
}
# videos = {}
#
# def abort_video_id_not_exist(video_id):
#     if video_id not in videos:
#         abort(404,message="Video id is not valid....")
#
# def abort_video_id_exist(video_id):
#     if video_id in videos:
#         abort(409,message="Video already exists with that id....")

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        #abort_video_id_not_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        #print(result)
        if not result:
            abort(404, message="Video ID not found....")
        return result
        #return videos[video_id]

    @marshal_with(resource_fields)
    def put(self,video_id):
        #abort_video_id_exist(video_id)
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID taken....")
        video = VideoModel(id=video_id,name=args["name"],views=args["views"],likes=args["likes"])
        db.session.add(video)
        db.session.commit()
        return video, 201
        #print(request.form["likes"])
        #videos[video_id] = args
        #return videos[video_id], 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="ID not found cannot update....")

        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        #db.session.add(result)
        db.session.commit()

        return result


    def delete(self, video_id):
        #abort_video_id_not_exist(video_id)
        #del videos[video_id]
        return " ", 204


api.add_resource(Video,"/video/<int:video_id>")
# names = {"Tim":{"Age":19,"Gender":"Male"},
#          "Nivesh":{"Age":28,"Gender":"Male"}}
#
# class HelloWorld(Resource):
#     def get(self,name):
#         #return {"name":name,"test":test}
#         return names[name]
#
#     def post(self):
#         return {"data":"Data Posted"}

#api.add_resource(HelloWorld,"/helloworld/<string:name>")

if __name__=="__main__":
    app.run(debug=True)