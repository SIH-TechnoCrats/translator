from flask import Flask, request, send_file
from flask_restful import Api, Resource
import os
import json
#from videototext import VideoTranslator
app = Flask(__name__)
api = Api(app)

class VideoUpload(Resource):
    def post(self):
        try:
            # Check if the 'video' field is in the request
            if 'video' not in request.files:
                return {'message': 'No file part'}, 400

            video_file = request.files['video']

            # Check if a file was uploaded
            if video_file.filename == '':
                return {'message': 'No selected file'}, 400

            # Check if the file extension is valid (MP4)
            if video_file.filename.endswith('.mp4'):
                # Save the file to a desired location
                video_file.save("file.mp4")
                #translator = VideoTranslator("file.mp4", "73aa00a13a4b4784ae4cb86be3a91cba", "eastus")
                #translator.translate_and_synthesize("convert.wav")



                return {'message': 'File uploaded successfully'}, 200
            else:
                return {'message': 'Invalid file format'}, 400
        except Exception as e:
            return {'error': str(e)}, 500

class language(Resource):
    def get(self):
        try:
            param_list = request.args.get('param_list')
            if len(param_list) == 0:
                return {"message": "Select language"},400
            elif len(param_list) > 0:
                with open("language.json", "w") as json_file:
                    json.dump(param_list.split(','),json_file)
                return {"message": "Received parameter list"},200

        except Exception as e:
            return {'error': str(e)}, 500

class VideoDownload(Resource):
    def get(self):
       # lan = request.args.get('lan')
        #file_path = 'final'+lan+".mp4"  # Update with the actual file path
        with open('language.json','r') as json_file:
            lan = json.load(json_file)
        file_path = 'final'+lan[0]+'.mp4'
        return send_file(file_path, as_attachment=True)

api.add_resource(VideoUpload, '/upload')
api.add_resource(VideoDownload, '/download')
api.add_resource(language, '/language')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)

