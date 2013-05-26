# -*- coding: utf-8 -*-
import subprocess
from burp import IBurpExtender, IMessageEditorTab, IMessageEditorTabFactory


CONTENT_PROTOBUF = 'application/x-protobuf'


class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    EXTENSION_NAME = "Protobuf Editor"

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()

        callbacks.setExtensionName(self.EXTENSION_NAME)
        callbacks.registerMessageEditorTabFactory(self)

        self.enabled = False
        code = subprocess.check_call(['protoc', '--version'],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        self.enabled = code == 0
        return

    def createNewInstance(self, controller, editable):
        return ProtobufEditor(self, controller, editable)


class ProtobufEditor(IMessageEditorTab):
    TAB_CAPTION = "Protobuf"

    def __init__(self, extender, controller, editable):
        self.extender = extender
        self.helpers = extender.helpers
        self.controller = controller
        self.editable = editable

        self._current = None

        self.editor = extender.callbacks.createTextEditor()
        self.editor.setEditable(editable)

    def getTabCaption(self):
        return self.TAB_CAPTION

    def getUiComponent(self):
        return self.editor.getComponent()

    def isEnabled(self, content, isRequest):
        if not self.extender.enabled:
            return False

        if isRequest:
            headers = self.helpers.analyzeRequest(content).getHeaders()
        else:
            headers = self.helpers.analyzeResponse(content).getHeaders()

        # first header is the request/response line
        for header in headers[1:]:
            if header.lower().startswith('content-type:'):
                value = header.split(':', 1)[1].strip()
                if value.lower() == CONTENT_PROTOBUF:
                    return True

        return False

    def setMessage(self, content, isRequest):
        if content is None:
            self.editor.setText(None)
            self.editor.setEditable(False)
            return

        if isRequest:
            offset = self.helpers.analyzeRequest(content).getBodyOffset()
        else:
            offset = self.helpers.analyzeResponse(content).getBodyOffset()

        body = content[offset:]

        process = subprocess.Popen(['protoc', '--decode_raw'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        try:
            output, error = process.communicate(body)
        except OSError:
            pass
        finally:
            if process.poll() != 0:
                process.kill()

        if error:
            raise Exception(err)

        self.editor.setText(output)
        # no current way to reserialize a message without a proto descriptor
        #self.editor.setEditable(self.editable)
        self.editor.setEditable(False)
        self._current = content
        return

    def getMessage(self):
        return self._current

    def isModified(self):
        return self.editor.isTextModified()

    def getSelectedData(self):
        return self.editor.getSelectedText()
