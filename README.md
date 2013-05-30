burp-protobuf-decoder
=====================

A simple Google Protobuf Decoder for Burp


Prerequisites
-------------

1. Download and install the [protoc](https://code.google.com/p/protobuf/).
2. Burp Professional 1.5.01+


Install
-------

1. In Burp Extender tab under Options > Python Environment,
    specify *Lib* as a folder for loading modules (or add contents of *Lib*
    to whatever folder you've already specified).

1. In Burp Extender tab, click Add
1. Select the Extension type: Python
1. Select the `protoburp.py` file
1. Click Next

The extension should be installed.


Frequently Asked Questions
--------------------------

1. Why can't I edit a decoded proto message?

	> Serializing a message requires a proto file descriptor (\*.proto file).
	> Without this proto, we don't know how fields should be serialized.

1. What if I have a proto file descriptor?

	> Load it from a Protobuf tab by right-clicking. Messages will
	> automatically decode from then on. If you wish to manually
	> deserialize as another type, this option is available to you via a
	> right-click context menu once a proto is loaded.

	> By loading a .proto, you can also edit/tamper that deserialize messages
	> and they'll be serialized properly for you when sent along.
