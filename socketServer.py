import websockets
import asyncio
import random
import os
import subprocess



scaProcessingPath = '/home/mcall/SCATEMPIN/'
scaOutputPath = '/home/aaron/SCATEMPOUT/'

async def hello(websocket, path):
    #generate a random sequence of numbers for the user ID
    userID = random.randint(0,10000000000000000000)
    userID = str(userID)
    #create a folder for the user
    data = await websocket.recv()
    #save the data to a file
    with open(scaProcessingPath + '/' + userID + '.cpp', 'w') as f:
        f.write(data)
        f.close()
    print ('file written')
    #Run SCA on the data
    
    #open the SCA output file
    try:
        with open(scaOutputPath + '/' + userID + '.html', 'r') as f:
            scaOutput = f.read()
            f.close()
            os.remove(scaProcessingPath + '/' + userID + '.cpp')
            os.remove(scaOutputPath + '/' + userID + '.html')
    except:
        scaOutput = 'Error: SCA did not run correctly'

        print('sca error')
    cssStuff = '''
<style>
.columnContainer{
  float: left;
  width: 50%;
  margin-bottom: 2rem;
  color: #f1c40f;
  
}

.sourcecode{
  position: relative;
  border-radius: 15px;
  border: 1px solid;
  border-color: #f1c40f;
  background-color: #1f2833;
  padding: 20px;
  width: 90%;
  margin: 0;
  font-family: "Lucida Console";
  color:#f1c40f;
}

.components{
  font-size: 32px;
  display: inline-flex;
  width: 1400px;
  flex-wrap: wrap;
  flex-direction: row;
  margin-top: 1rem;
  color: #f1c40f;
}

.components > p {
  width: 1400px;
  text-align: center;
  margin-bottom: 1rem;
  color: #f1c40f;
}

.correctComponent{
  position: relative;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  border: 1px solid #66e766;
  padding: 20px;
  max-width: 45%;
  height: auto;
  margin: 5px;
  font-family: "Lucida Console";
  font-size: 16px;
  color: #f1c40f;
}

.wrongComponent{
  position: relative;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  border: 1px solid #eb4040;
  padding: 20px;
  max-width: 45%;
  height: auto;
  margin: 5px;
  font-family: "Lucida Console";
  font-size: 16px;
  color: #f1c40f;
}

.rule
{
  position: relative;
  border-radius: 25px;
  border: 1px solid;    scaOutput.
  color: #fffbfc;
  font-family: "Lucida Console";
}
.titleText {
  font-size: 2rem;
  margin-bottom: -1rem;
  text-align: center;
  color: #f1c40f;
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
  margin-right: 1.5rem    scaOutput.

{
  position: relative;
  border-radius: 20px;
  border: 1px solid;
  padding: 5px;
  width: 90%;
  height: 530px;
  margin: 0;cmdOutput
}

#rcorners {
    border-radius: 25px;
    border: 1px solid #227db3;
    padding: 20px;
    width: 200px;
    height: 150px;
    color: #f1c40f;
  }

  h1{
    font-size: 32px;
    color: #f1c40f;
  }

  h2{
    font-style: italic;
    font-size: 2cmdOutput0px;
    color: #f1c40f;
  }

  </style>'''
    scaOutput = scaOutput.replace(str(userID) + '.cpp', '' )
    scaOutput = scaOutput.replace('<link rel="stylesheet" href="../../core/src/htmlStyle.css">', '' )
    #attach styling to scaOutput
    scaOutput = cssStuff + scaOutput
    #send the SCA output to the user
    await websocket.send(scaOutput)
    #end the connection
    await websocket.close()



start_server = websockets.serve(hello, "localhost", 8008)



asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()