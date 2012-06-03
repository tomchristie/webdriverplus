from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement as _WebElement
#from selenium.webdriver.common.action_chains import ActionChains

from webdriverplus.selectors import SelectorMixin
from webdriverplus.utils import get_terminal_size
from webdriverplus.wrappers import Style, Attributes, Size, Location

import os
import sys


# http://stackoverflow.com/questions/6157929/how-to-simulate-mouse-click-using-javascript/6158050#6158050
def simulate_event(event, **options):
    return """
    function simulate(element, eventName)
    {
        var options = extend(defaultOptions, arguments[2] || {});
        var oEvent, eventType = null;

        for (var name in eventMatchers)
        {
            if (eventMatchers[name].test(eventName)) { eventType = name; break; }
        }

        if (!eventType)
            throw new SyntaxError('Only HTMLEvents and MouseEvents interfaces are supported');

        if (document.createEvent)
        {
            oEvent = document.createEvent(eventType);
            if (eventType == 'HTMLEvents')
            {
                oEvent.initEvent(eventName, options.bubbles, options.cancelable);
            }
            else
            {
                oEvent.initMouseEvent(eventName, options.bubbles, options.cancelable, document.defaultView,
          options.button, options.pointerX, options.pointerY, options.pointerX, options.pointerY,
          options.ctrlKey, options.altKey, options.shiftKey, options.metaKey, options.button, element);
            }
            element.dispatchEvent(oEvent);
        }
        else
        {
            options.clientX = options.pointerX;
            options.clientY = options.pointerY;
            var evt = document.createEventObject();
            oEvent = extend(evt, options);
            element.fireEvent('on' + eventName, oEvent);
        }
        return element;
    }

    function extend(destination, source) {
        for (var property in source)
          destination[property] = source[property];
        return destination;
    }

    var eventMatchers = {
        'HTMLEvents': /^(?:load|unload|abort|error|select|change|submit|reset|focus|blur|resize|scroll)$/,
        'MouseEvents': /^(?:click|dblclick|mouse(?:down|up|over|move|out))$/
    }
    var defaultOptions = {
        pointerX: 0,
        pointerY: 0,
        button: 0,
        ctrlKey: false,
        altKey: false,
        shiftKey: false,
        metaKey: false,
        bubbles: true,
        cancelable: true
    }

    simulate(arguments[0], "%s", %s);""" % (event, repr(options))


class WebElement(SelectorMixin, _WebElement):
    @property
    def _xpath_prefix(self):
        return './/*'

    # Traversal
    def parent(self, *args, **kwargs):
        """
        Note: We're overriding the default WebElement.parent behaviour here.
        (Normally .parent is a property that returns the WebDriver object.)
        """
        ret = self.find(xpath='..')
        return ret.filter(*args, **kwargs)

    def children(self, *args, **kwargs):
        ret = self.find(xpath='./*')
        return ret.filter(*args, **kwargs)

    def descendants(self):
        return self.find(xpath='./descendant::*')

    def ancestors(self, *args, **kwargs):
        ret = self.find(xpath='./ancestor::*')
        return ret.filter(*args, **kwargs)

    def next(self, *args, **kwargs):
        ret = self.find(xpath='./following-sibling::*[1]')
        return ret.filter(*args, **kwargs)

    def prev(self, *args, **kwargs):
        ret = self.find(xpath='./preceding-sibling::*[1]')
        return ret.filter(*args, **kwargs)

    def next_all(self, *args, **kwargs):
        ret = self.find(xpath='./following-sibling::*')
        return ret.filter(*args, **kwargs)

    def prev_all(self, *args, **kwargs):
        ret = self.find(xpath='./preceding-sibling::*')
        return ret.filter(*args, **kwargs)

    def siblings(self, *args, **kwargs):
        ret = self.prev_all() | self.next_all()
        return ret.filter(*args, **kwargs)

    # Inspection & Manipulation
    @property
    def id(self):
        return self.get_attribute('id')

    @property
    def type(self):
        return self.get_attribute('type')

    @property
    def value(self):
        return self.get_attribute('value')

    @property
    def is_checked(self):
        return self.get_attribute('checked') is not None

    @property
    def is_selected(self):
        return super(WebElement, self).is_selected()

    @property
    def is_displayed(self):
        return super(WebElement, self).is_displayed()

    @property
    def is_enabled(self):
        return super(WebElement, self).is_enabled()

    @property
    def inner_html(self):
        return self.get_attribute('innerHTML')

    @property
    def html(self):
        # http://stackoverflow.com/questions/1763479/how-to-get-the-html-for-a-dom-element-in-javascript
        script = """
            var container = document.createElement("div");
            container.appendChild(arguments[0].cloneNode(true));
            return container.innerHTML;
        """
        return self._parent.execute_script(script, self)

    @property
    def index(self):
        return len(self.prev_all())

    @property
    def style(self):
        return Style(self)

    @property
    def size(self):
        val = super(WebElement, self).size
        return Size(val['width'], val['height'])

    @property
    def location(self):
        val = super(WebElement, self).location
        return Location(val['x'], val['y'])

    @property
    def attributes(self):
        return Attributes(self)

    def javascript(self, script):
        script = "return arguments[0].%s;" % script
        return  self._parent.execute_script(script, self)

    def jquery(self, script):
        script = "return $(arguments[0]).%s;" % script
        return  self._parent.execute_script(script, self)

    # Actions...
    # Native events not supported on mac.
    def double_click(self):
        self._parent.execute_script(simulate_event('dblclick'), self)
        #ActionChains(self._parent).double_click(self).perform()

    def context_click(self):
        self._parent.execute_script(simulate_event('click', button=2), self)
        #ActionChains(self._parent).double_click(self).perform()

    def click_and_hold(self):
        self._parent.execute_script(simulate_event('mousedown'), self)
        #ActionChains(self._parent).click_and_hold(self).perform()

    def release(self):
        self._parent.execute_script(simulate_event('mouseup'), self)
        #ActionChains(self._parent).click_and_hold(self).perform()

    def move_to(self):
        self._parent.execute_script(simulate_event('mouseover'), self)
        #ActionChains(self._parent).move_to_element(self).perform()

    def __repr__(self):
        try:
            if os.isatty(sys.stdin.fileno()):
                try:
                    width = get_terminal_size()[0]
                except:
                    width = 80
            else:
                width = 80

            ret = self.html
            ret = ' '.join(ret.split())
            ret = ret.encode('utf-8')

            if len(ret) >= width - 2:
                ret = ret[:width - 5] + '...'
            #self.style.backgroundColor = '#f9edbe'
            #self.style.borderColor = '#f9edbe'
            #self.style.outline = '1px solid black'
            return ret
        except StaleElementReferenceException:
            return '<StaleElement>'

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id
