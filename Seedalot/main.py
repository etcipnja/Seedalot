from Farmware import *

APP_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep))-3]).replace('-master','')

class Seedalot(Farmware):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Farmware.__init__(self,((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '').replace('-dev', ''))

    # ------------------------------------------------------------------------------------------------------------------
    def load_config(self):

        super(Seedalot, self).load_config()

        self.get_arg('operation', "remove")
        self.get_arg('xy', (0,0))
        self.get_arg('rows', 4)
        self.get_arg('cols', 2)

        if self.args['rows'] < 0 or self.args['rows'] > 20 or self.args['cols'] < 0 or self.args['cols'] > 20:
            raise ValueError('Invalid rows {} or columns {}. Expecting a number 0-20'.format(self.args['rows'],
                                                                                                 self.args['cols']))
        if self.args['operation'] not in ["log","add","remove"]:
            raise ValueError('Invalid operation [{}]'.format(self.args['operation']))
        if self.args['operation']=='log': self.debug=True

        self.log(str(self.args))


    # ------------------------------------------------------------------------------------------------------------------
    def log_point(self, point, message='\t'):
        self.log('{0:s} ({1:4d},{2:4d}) {3:s}'.format(message, point['x'], point['y'], point['name']))

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):

        try: point = next(p for p in self.points()
                          if p['x'] == int(self.args['xy'][0]) and p['y'] == int(self.args['xy'][1])
                          and p['pointer_type'].lower()=='plant').copy()
        except: raise ValueError('Plant is not found @ {}'.format(self.args['xy']))
        self.log_point(point, 'Original plant: ')

        #query openfarm for row_spacing
        r=self.lookup_openfarm(point)['data'][0]['attributes']['row_spacing'] * 10

        ids = ''
        sy = point['y']
        for i in range(self.args['cols']):
            point['y'] = sy
            for j in range(self.args['rows']):
                if i != 0 or j != 0:

                    try: existing_id = next(p for p in self.points() if p['x'] == point['x'] and p['y'] == point['y'])['id']
                    except: existing_id=0

                    if self.args['operation'].lower() == 'log':  #Loging only
                        self.log_point(point,'Considered: ')
                    elif self.args['operation'].lower()=='add':  #Adding a plant
                            if existing_id==0:
                                self.log_point(point,'Adding: ')
                                self.post('points',point)
                            else:
                                self.log('Something already planted @ ({},{})'.format(point['x'],point['y']),'warn')
                    elif self.args['operation'].lower() == 'remove': # Removing a plant
                        if existing_id!=0:
                            if len(ids) != 0: ids += ','
                            ids += str(existing_id)
                        else: self.log('Plant is not found, but it is ok @ {},{}'.format(point['x'],point['y']),'warn')
                    else:
                        raise ValueError('Unknown action: {}'.format(self.args['action']))

                    # actually deleting if there is something to delete
                    if (i==self.args['cols']-1 and j==self.args['rows']-1 and len(ids) != 0) or ids.count(',')>=19:
                        self.log('Removing {} plants'.format(ids.count(',') + 1))
                        self.delete('points/{}'.format(ids))
                        ids = ''
                point['y'] += r
            point['x'] += r



# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    app = Seedalot()
    try:
        app.load_config()
        app.run()
        sys.exit(0)

    except NameError as error:
        app.log('SYNTAX!: {}'.format(str(error)), 'error')
        raise
    except requests.exceptions.HTTPError as error:
        app.log('HTTP error {} {} '.format(error.response.status_code,error.response.text[0:100]), 'error')
    except Exception as e:
        app.log('Something went wrong: {}'.format(str(e)), 'error')
    sys.exit(1)



