# credit: mikaelho / pythonista – gestures
# credit: tdamdouni / Pythonista
# credit: Pythonista / slider / SliderWithLabel_danrcook.py


class AugmentedSliderWithLabel(ui.View):
    '''wrapper for ui.Slider to also show a label. You can edit the value of the slider directly in the label since it is a textfield. Can take the following keyword arguments:
        - for the slider:
            >> value: default value when presented (should be a number that is less than max_val and greater than 0). The default is 50
            >> max_val: the default for a usual slider is 1.0. SliderWithLabel will conventiently multiply the max_val for the label display and for returning it's value attribute. The default is 100
            >> tint_color for the color of the slider bar (up to current point). Default is 0.7 (gray)
        - values are rounded in the label and for SliderWithLabel.value
        - SliderWithLabel needs some vertical space: has a height of 60
        - use SliderWithLabel.value for return a value between 0 and SliderWithLabel.max_val
        
        khoitsma
        - AugmentedSliderWithLabel augmented class
        -    added attributes:
                min_val
                frame
                   moved this inside of the class definition
                secondaction
                   the original action for slider was to update self.label
                   I added an additional action to allow
                   an "outside of class" update
                name
                   I added a name to provide a means for easy referencing
                s_type
                   I added a slider type; can be:
                      int (as in the original class def)
                      float
                      boolean
                 round
                    I added a rounding value
                       0.5 rounds to nearest 0.5
                       5 rounds to nearest 5
                 group
                    I added a group to allow different functions 
                    for different groups
        - sample call
             g = AugmentedSliderWithLabel(
                    value = str(float(myview['rot'].text)), 
                    min_val = 0, 
                    max_val = 180,
                    frame = (144,329,110,60),
                    second_action = setvals,
                    name = 'rot',
                    s_type = 'round',
                    round = 5,
                    group = 'slider')
        '''

    
    def __init__(self, **kwargs):
        self.slider = ui.Slider()
        
        #defaults
        self.min_val = 0
        self.max_val = 10
        
        self.s_type = kwargs.get('s_type', 'int')
        self.name = kwargs.get('name', 'unnamed')
        self.group = kwargs.get('group', 'ungrouped')
        self.second_action = kwargs.get('second_action', None)
        self.round = kwargs.get('round', 1)
        self.frame = kwargs.get('frame', (0,0,100,60))

        self.max_val = kwargs.get('max_val', self.max_val)
        self.min_val = kwargs.get('min_val', self.min_val)

        self.slider.value = (float(self.bool_to_str(kwargs['value']))-self.min_val)/(self.max_val-self.min_val) if 'value' in kwargs else 0.5*(self.max_val-self.min_val)

        self.value = round(self.slider.value*(self.max_val-self.min_val)+self.min_val) #for convenience in getting the value attribute

        self.slider.action = self.update_label_and_value
        self.slider.tint_color = kwargs.get('tint_color', 0.7)

        self.label = ui.TextField()
        self.label.action = self.update_value
        self.label.bordered = True
        self.label.alignment = ui.ALIGN_CENTER
        self.label.font = ('<system>',11)
        self.label.text_color = 0.7
        self.label.text = str(self.value)
        self.add_subview(self.slider)
        self.add_subview(self.label)
        self.border_color = 0.7

                
    def update_value(self, sender):
        try:             #try/except in case wrong text is entered...
            self.slider.value = (float(self.label.text)-self.min_val)/(self.max_val- self.min_val)
            self.update_label_and_value(self)
        except:
            pass


    def update_label_and_value(self, sender):    
        self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17 
        self.value = float(self.slider.value*(self.max_val-self.min_val)+self.min_val)
        try:
            if self.s_type == 'boolean':
                if self.value <= 0.5*(self.max_val - self.min_val):
                    self.label.text = 'False'
                else:
                    self.label.text = 'True'
            elif self.s_type == 'integer':
                self.label.text = str(self.myround(self.value, 1))
            elif self.s_type == 'round':
                self.label.text = str(self.myround(self.value, self.round))
            else:
                self.label.text = str(self.value)
        except:
            self.label.text = str(self.value)
        if self.label.x + self.label.width > self.width:
            self.label.x = self.width - self.label.width
        if self.label.x < 0:
            self.label.x = 0
        if self.second_action:
        	self.second_action(self.name, self.label.text)

        
    def draw(self):
        self.height = 60
        self.slider.frame = (0,self.height/2-7,self.width, 34)
        self.label.width, self.label.height = 46, 20
        self.label.y = self.slider.y - (self.label.height + 2)
        self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17


    def myround(self, x, base = 5):
        return base * round(float(x)/base)
    
    
    def bool_to_str(self, x):
        if x.upper() == 'TRUE':
            return '1'
        elif x.upper() == 'FALSE':
            return '0'
        else:
            return x
