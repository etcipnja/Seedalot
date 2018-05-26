from Farmware import *

APP_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep))-3]).replace('-master','')

class Seedalot():
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Farmware.__init__(self,((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '').replace('-dev', ''))

    # ------------------------------------------------------------------------------------------------------------------
    def load_config(self):

        super(Farmware, self).load_config()

        self.get_arg('action', "log")
        self.get_arg('xy', (0,0))
        self.get_arg('rows', 0)
        self.get_arg('cols', 0)

        if rows < 0 or rows > 20 or cols < 0 or cols > 20:
            raise ValueError('Invalid rows ({}) or columns ({}). Expecting a number 0-20'.format(self.params['rows'],
                                                                                                 self.params['cols']))
        self.log(str(self.args))


    # ------------------------------------------------------------------------------------------------------------------
    def log_point(self, point, message='\t'):
        self.log('{0:s} ({1:4d},{2:4d}) {3:s}'.format(message, point['x'], point['y'], point['name']))

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):

        #validate input parameters
        try:
            rows=int(self.params['rows'])
            cols=int(self.params['cols'])
            if rows<0 or rows>20 or cols<0 or cols>20: raise ValueError
        except:
            raise ValueError('Invalid rows ({}) or columns ({}). Expecting a number 0-20'.format(self.params['rows'],self.params['cols']))

        #get points from the server
        response = requests.get(self.api_url + 'points', headers=self.headers)
        self.handle_error(response)
        points=response.json()

        try: point = next(p for p in points
                          if p['x'] == int(self.params['x']) and p['y'] == int(self.params['y'])
                          and p['pointer_type'].lower()=='plant').copy()
        except: raise ValueError('Plant is not found @ ({},{})'.format(self.params['x'],self.params['y']))
        self.log_point(point, 'Original plant: ')

        #query openfarm for row_spacing
        response = requests.get(
            'https://openfarm.cc/api/v1/crops?include=pictures&filter={}'.format(point['openfarm_slug']),
            headers=self.headers)
        self.handle_error(response)
        plant = response.json()
        r = plant['data'][0]['attributes']['row_spacing'] * 10
        #s = plant['data'][0]['attributes']['spread'] * 10

        #main sequence
        ids = ''
        sy = point['y']
        for i in range(cols):
            point['y'] = sy
            for j in range(rows):
                if i != 0 or j != 0:
                    try: existing_id = next(p for p in points if p['x'] == point['x'] and p['y'] == point['y'])['id']
                    except: existing_id=0
                    #Logging only
                    if self.params['action'].lower() == 'log':
                        self.log_point(point,'Considered: ')
                    #Adding a plant
                    else:
                        if self.params['action'].lower()=='add':
                            if existing_id==0:
                                self.log_point(point,'Adding: ')
                                response = requests.post(self.api_url + 'points', headers=self.headers, data=json.dumps(point))
                                self.handle_error(response)
                            else:
                                self.log('Something already planted @ ({},{})'.format(point['x'],point['y']),'warn')
                    # Removing a plant
                        else:
                            if self.params['action'].lower() == 'remove':
                                if existing_id!=0:
                                    if len(ids) != 0: ids += ','
                                    ids += str(existing_id)
                                else: self.log('Plant is not found, but it is ok @ {},{}'.format(point['x'],point['y']),'warn')
                            else:
                                raise ValueError('Unknown action: {}'.format(self.params['action']))
                            # actually deleting if there is something to delete
                            if (i==cols-1 and j==rows-1 and len(ids) != 0) or ids.count(',')>=19:
                                    self.log('Removing {} plants'.format(ids.count(',') + 1))
                                    response = requests.delete(self.api_url + 'points/{}'.format(ids),
                                                               headers=self.headers)
                                    self.handle_error(response)
                                    ids = ''
                point['y'] += r
            point['x'] += r



# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    try:
        app=Seedalot()
        app.run()

    except Exception as e:
        try:
            app.log('Something went wrong: {}'.format(str(e)),'error')
        except:
            print('Something really bad happened: {}.'.format(e))



