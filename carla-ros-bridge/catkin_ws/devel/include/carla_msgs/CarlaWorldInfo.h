// Generated by gencpp from file carla_msgs/CarlaWorldInfo.msg
// DO NOT EDIT!


#ifndef CARLA_MSGS_MESSAGE_CARLAWORLDINFO_H
#define CARLA_MSGS_MESSAGE_CARLAWORLDINFO_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace carla_msgs
{
template <class ContainerAllocator>
struct CarlaWorldInfo_
{
  typedef CarlaWorldInfo_<ContainerAllocator> Type;

  CarlaWorldInfo_()
    : map_name()
    , opendrive()  {
    }
  CarlaWorldInfo_(const ContainerAllocator& _alloc)
    : map_name(_alloc)
    , opendrive(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _map_name_type;
  _map_name_type map_name;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _opendrive_type;
  _opendrive_type opendrive;





  typedef boost::shared_ptr< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> const> ConstPtr;

}; // struct CarlaWorldInfo_

typedef ::carla_msgs::CarlaWorldInfo_<std::allocator<void> > CarlaWorldInfo;

typedef boost::shared_ptr< ::carla_msgs::CarlaWorldInfo > CarlaWorldInfoPtr;
typedef boost::shared_ptr< ::carla_msgs::CarlaWorldInfo const> CarlaWorldInfoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator1> & lhs, const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator2> & rhs)
{
  return lhs.map_name == rhs.map_name &&
    lhs.opendrive == rhs.opendrive;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator1> & lhs, const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace carla_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "7a3a7a7fc8c213a8bec2ce7928b0a46c";
  }

  static const char* value(const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x7a3a7a7fc8c213a8ULL;
  static const uint64_t static_value2 = 0xbec2ce7928b0a46cULL;
};

template<class ContainerAllocator>
struct DataType< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "carla_msgs/CarlaWorldInfo";
  }

  static const char* value(const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#\n"
"# Copyright (c) 2018-2019 Intel Corporation.\n"
"#\n"
"# This work is licensed under the terms of the MIT license.\n"
"# For a copy, see <https://opensource.org/licenses/MIT>.\n"
"#\n"
"\n"
"string map_name\n"
"string opendrive\n"
;
  }

  static const char* value(const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.map_name);
      stream.next(m.opendrive);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CarlaWorldInfo_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::carla_msgs::CarlaWorldInfo_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::carla_msgs::CarlaWorldInfo_<ContainerAllocator>& v)
  {
    s << indent << "map_name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.map_name);
    s << indent << "opendrive: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.opendrive);
  }
};

} // namespace message_operations
} // namespace ros

#endif // CARLA_MSGS_MESSAGE_CARLAWORLDINFO_H
