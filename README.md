burp-protobuf-decoder
=====================

A simple Google Protobuf Decoder for Burp


Install
-------

1. In Burp Extender tab, click Add
2. Select the Extension type: Python
3. Select the `protoburp.py` file
4. Click Next

The extension should be installed.


Frequently Asked Questions
--------------------------

1. Why can't I edit a decoded proto message?

> Serializing a message requires a proto file descriptor (\*.proto file).
> Without this proto, we don't know how fields should be serialized.

2. What if I have a proto file descriptor?

> Well then, I hope to one day support creating proto messages from a proto
> file descriptor at runtime.
