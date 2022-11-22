from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from Interface_TypeInference.Type_Inference import main_func

app = Flask(__name__)
CORS(app)

@app.route('/login',methods = ['POST','GET'])
def login():
   if request.method == 'POST':
      data = request.form
      print(data)
      code = data['co_area']
      sim_name = data['co_name']
      sim_name = sim_name.split("\n")
      top = data['co_top'].replace("top-", "")
      opt = data['co_all']
      model = data["model"]
      print(code)
      print(sim_name)
      print(top)
      print(opt)
      print(model)
      pro_code = main_func(code, sim_name, top, opt, model)
      if opt != "1":
         pro_code = pro_code.split("<br/>")
         return {"pro_code": pro_code}
      print("pro_code: " + str(pro_code))
      return pro_code

if __name__ == '__main__':
   app.run(debug=True)

