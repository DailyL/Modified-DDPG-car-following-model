# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from carla_ackermann_msgs/EgoVehicleControlMaxima.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class EgoVehicleControlMaxima(genpy.Message):
  _md5sum = "9895ba8c0c51c81d773f7d191f9aeb3e"
  _type = "carla_ackermann_msgs/EgoVehicleControlMaxima"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """#
# Copyright (c) 2018-2019 Intel Corporation.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
# This represents some ego vehicle control maximal values

# vehicle maximum values
float32 max_steering_angle
float32 max_speed
float32 max_accel
float32 max_decel
float32 min_accel
float32 max_pedal
"""
  __slots__ = ['max_steering_angle','max_speed','max_accel','max_decel','min_accel','max_pedal']
  _slot_types = ['float32','float32','float32','float32','float32','float32']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       max_steering_angle,max_speed,max_accel,max_decel,min_accel,max_pedal

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(EgoVehicleControlMaxima, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.max_steering_angle is None:
        self.max_steering_angle = 0.
      if self.max_speed is None:
        self.max_speed = 0.
      if self.max_accel is None:
        self.max_accel = 0.
      if self.max_decel is None:
        self.max_decel = 0.
      if self.min_accel is None:
        self.min_accel = 0.
      if self.max_pedal is None:
        self.max_pedal = 0.
    else:
      self.max_steering_angle = 0.
      self.max_speed = 0.
      self.max_accel = 0.
      self.max_decel = 0.
      self.min_accel = 0.
      self.max_pedal = 0.

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_6f().pack(_x.max_steering_angle, _x.max_speed, _x.max_accel, _x.max_decel, _x.min_accel, _x.max_pedal))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 24
      (_x.max_steering_angle, _x.max_speed, _x.max_accel, _x.max_decel, _x.min_accel, _x.max_pedal,) = _get_struct_6f().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_6f().pack(_x.max_steering_angle, _x.max_speed, _x.max_accel, _x.max_decel, _x.min_accel, _x.max_pedal))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 24
      (_x.max_steering_angle, _x.max_speed, _x.max_accel, _x.max_decel, _x.min_accel, _x.max_pedal,) = _get_struct_6f().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_6f = None
def _get_struct_6f():
    global _struct_6f
    if _struct_6f is None:
        _struct_6f = struct.Struct("<6f")
    return _struct_6f
