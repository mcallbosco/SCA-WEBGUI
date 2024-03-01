import websockets
import asyncio
import random
import os
import subprocess
import ssl


scaProcessingPath = '/home/ubuntu/SCAIN'
scaOutputPath = '/home/ubuntu/SCAOUT'
scaPath = "/home/ubuntu/SCA/SCA/core/src/a.out"

async def hello(websocket, path):
    skipCSS = False
    #generate a random sequence of numbers for the user ID
    userID = random.randint(0,10000000000000000000)
    userID = str(userID)
    #create a folder for the user
    data = await websocket.recv()
    #make sure the file is not too large
    if (len(data) > 1000000):
        await websocket.send('Error: File too large')
        await websocket.close()
        return
    #save the data to a file
    with open(scaProcessingPath + '/' + userID + '.cpp', 'w') as f:
        f.write(data)
        f.close()
    print ('file written')
    #Run SCA on the data
    try:
        output = subprocess.check_output([scaPath, scaProcessingPath + '/' + userID + '.cpp', scaOutputPath + '/' + userID + '.html'], universal_newlines=True)
    except:
        print('sca error bad exit code')
        output = "Error: server error"
        
    #open the SCA output file
    try:
        with open(scaOutputPath + '/' + userID + '.html', 'r') as f:
            scaOutput = f.read()
            f.close()
            os.remove(scaProcessingPath + '/' + userID + '.cpp')
            os.remove(scaOutputPath + '/' + userID + '.html')
    except:
        scaOutput = 'Error: SCA did not run correctly. If this error is not due to the uploaded code, please contact the website admin. Here is the logs: ' + output
        skipCSS = True

    cssStuff = '''
<style>
.columnContainer{
    float: left;
    width: 50%;
    margin-bottom: 2rem;
}

.sourcecode{
  position: relative;
  border-radius: 25px;
  border: 2px solid;
  background-color: #beddf0;
  padding: 20px;
  width: 90%;
  margin: 0;
  font-family: "Lucida Console";
}

.components{
  font-size: 32px;
  display: inline-flex;
  width: 1400px;
  flex-wrap: wrap;
  flex-direction: row;
  margin-top: 1rem;
}

.components > p {
  width: 1400px;
  text-align: center;
  margin-bottom: 1rem;
}

.correctComponent{
  position: relative;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  border: 2px solid #66e766;
  padding: 20px;
  max-width: 45%;
  height: auto;
  margin: 5px;
  font-family: "Lucida Console";
  font-size: 16px;
}

.wrongComponent{
  position: relative;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  border: 2px solid #eb4040;
  padding: 20px;
  max-width: 45%;
  height: auto;
  margin: 5px;
  font-family: "Lucida Console";
  font-size: 16px;
}

.rule
{
  position: relative;
  border-radius: 25px;
  border: 2px solid;
  padding: 20px;
  width: 90%;
  margin-top: .5rem;
  font-family: "Lucida Console";
}
.titleText {
  font-size: 2rem;
  margin-bottom: -1rem;
  text-align: center;
}
.entirePage {
  width: 1400px;
  margin: auto;
}

.componentContainer {
  padding: 1rem;
  border: 1px solid black;
  border-radius: 1rem;
  background-color: rgb(230,230,230);
  margin-right: 1.5rem;
}

.ruleContainer
{
  position: relative;
  border-radius: 20px;
  border: 2px solid;
  padding: 5px;
  width: 90%;
  height: 530px;
  margin: 0;
}

#rcorners {
    border-radius: 25px;
    border: 2px solid #227db3;
    padding: 20px;
    width: 200px;
    height: 150px;
  }

  h1{
    font-size: 32px;
  }

  h2{
    font-style: italic;
    font-size: 20px;
  }


  </style>'''
    if (not skipCSS):
      scaOutput = scaOutput.replace(str(userID) + '.cpp', '' )
      scaOutput = scaOutput.replace('<link rel="stylesheet" href="../../core/src/htmlStyle.css">', '' )
      #attach styling to scaOutput
      scaOutput = cssStuff + scaOutput
    #send the SCA output to the user
    await websocket.send(scaOutput)
    #end the connection
    await websocket.close()



ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="~/apache-selfsigned.crt", keyfile="~/apache-selfsigned.key")

start_server = websockets.serve(hello, "172.31.0.162", 8008, ssl = ssl_context)



asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()