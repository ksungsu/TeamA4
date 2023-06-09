from flask import Flask, render_template, request, jsonify, redirect
app = Flask(__name__)

import certifi
import base64
import gridfs

from bson.objectid import ObjectId

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.awfowzp.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

fs = gridfs.GridFS(db)
ca = certifi.where()

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/api", methods=["GET"])
def home_get():
   all_myself = list(db.myself.find({},{'_id':True, 'name':True, 'mbti':True, 'introduction':True, 
                                         'strengths':True, 'collaboration_style':True ,'blog_url':True
                                         ,'github_url':True, 'photo':True}))
    
   for myself in all_myself:
        photo_id = myself['photo']
        if photo_id:
           try:
              image_data = fs.get(photo_id).read()
              base64_img = base64.b64encode(image_data).decode('utf-8')
              myself['photo'] = 'data:image/jpeg;base64,' + base64_img
           except gridfs.error.NoFile as e:
              print.error("파일이 없습니다.")  
                 
        myself['_id'] = str(myself['_id'])
    
   return jsonify({'result':all_myself})

@app.route("/api/new", methods=["GET"])
def get_write():

   return render_template('write.html')

@app.route("/api/new", methods=["POST"])
def post_write():
       
    video_receive = request.files['video_give']   
    photo_receive = request.files['photo_give']
    name_receive = request.form['name_give']
    mbti_receive = request.form['mbti_give']
    introduction_receive = request.form['introduction_give']
    strengths_receive = request.form['strengths_give']
    collaboration_style_receive = request.form['collaboration-style_give']
    blog_url_receive = request.form['blog-url_give']
    github_receive = request.form['github-url_give']

    file_img_id = fs.put(photo_receive)
    file_video_id = fs.put(video_receive)
    
    doc = {
       'video' : file_video_id,
       'photo' : file_img_id,
       'name' : name_receive,
       'mbti' : mbti_receive,
       'introduction' : introduction_receive,
       'strengths' : strengths_receive,
       'collaboration_style' : collaboration_style_receive,
       'blog_url' : blog_url_receive,
       'github_url' : github_receive,
    }
    
    db.myself.insert_one(doc)

    return redirect('/')
 
 
@app.route("/api/view/<id>", methods=["GET"])
def find_team(id):
    
    find_myself = db.myself.find_one({"_id": ObjectId(id)})
        
    photo_id = find_myself['photo']
    video_id = find_myself['video']
    
    print('find_myself = ', find_myself['photo'])
    
    print(photo_id)
      
    if photo_id:
         try:
              image_data = fs.get(photo_id).read()
              base64_img = base64.b64encode(image_data).decode('utf-8')
              find_myself['photo'] = 'data:image/jpeg;base64,' + base64_img
         except gridfs.error.NoFile as e:
              print.error("파일이 없습니다.")
              
    if video_id:
         try:
              video_data = fs.get(video_id).read()
              base64_video = base64.b64encode(video_data).decode('utf-8')
              find_myself['video'] = 'data:video/jpeg;base64,' + base64_video
         except gridfs.error.NoFile as e:
              print.error("파일이 없습니다.")          
    
    find_myself['photo'] = str(find_myself['photo'])

    
    return render_template('view.html', myself=find_myself)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)