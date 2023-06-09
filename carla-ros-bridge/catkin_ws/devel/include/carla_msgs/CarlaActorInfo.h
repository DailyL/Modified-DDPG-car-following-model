// Generated by gencpp from file carla_msgs/CarlaActorInfo.msg
// DO NOT EDIT!


#ifndef CARLA_MSGS_MESSAGE_CARLAACTORINFO_H
#define CARLA_MSGS_MESSAGE_CARLAACTORINFO_H


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
struct CarlaActorInfo_
{
  typedef CarlaActorInfo_<ContainerAllocator> Type;

  CarlaActorInfo_()
    : id(0)
    , parent_id(0)
    , type()
    , rolename()  {
    }
  CarlaActorInfo_(const ContainerAllocator& _alloc)
    : id(0)
    , parent_id(0)
    , type(_alloc)
    , rolename(_alloc)  {
  (void)_alloc;
    }



   typedef uint32_t _id_type;
  _id_type id;

   typedef uint32_t _parent_id_type;
  _parent_id_type parent_id;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _type_type;
  _type_type type;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _rolename_type;
  _rolename_type rolename;





  typedef boost::shared_ptr< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> const> ConstPtr;

}; // struct CarlaActorInfo_

typedef ::carla_msgs::CarlaActorInfo_<std::allocator<void> > CarlaActorInfo;

typedef boost::shared_ptr< ::carla_msgs::CarlaActorInfo > CarlaActorInfoPtr;
typedef boost::shared_ptr< ::carla_msgs::CarlaActorInfo const> CarlaActorInfoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::carla_msgs::CarlaActorInfo_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::carla_msgs::CarlaActorInfo_<ContainerAllocator1> & lhs, const ::carla_msgs::CarlaActorInfo_<ContainerAllocator2> & rhs)
{
  return lhs.id == rhs.id &&
    lhs.parent_id == rhs.parent_id &&
    lhs.type == rhs.type &&
    lhs.rolename == rhs.rolename;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::carla_msgs::CarlaActorInfo_<ContainerAllocator1> & lhs, const ::carla_msgs::CarlaActorInfo_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace carla_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "101ec1019fd4e4a480a106d5c6d5dcac";
  }

  static const char* value(const ::carla_msgs::CarlaActorInfo_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x101ec1019fd4e4a4ULL;
  static const uint64_t static_value2 = 0x80a106d5c6d5dcacULL;
};

template<class ContainerAllocator>
struct DataType< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "carla_msgs/CarlaActorInfo";
  }

  static const char* value(const ::carla_msgs::CarlaActorInfo_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#\n"
"# Copyright (c) 2019 Intel Corporation.\n"
"#\n"
"# This work is licensed under the terms of the MIT license.\n"
"# For a copy, see <https://opensource.org/licenses/MIT>.\n"
"#\n"
"\n"
"uint32 id\n"
"uint32 parent_id # 0 if no parent available\n"
"string type\n"
"string rolename\n"
"\n"
;
  }

  static const char* value(const ::carla_msgs::CarlaActorInfo_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.parent_id);
      stream.next(m.type);
      stream.next(m.rolename);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CarlaActorInfo_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::carla_msgs::CarlaActorInfo_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::carla_msgs::CarlaActorInfo_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.id);
    s << indent << "parent_id: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.parent_id);
    s << indent << "type: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.type);
    s << indent << "rolename: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.rolename);
  }
};

} // namespace message_operations
} // namespace ros

#endif // CARLA_MSGS_MESSAGE_CARLAACTORINFO_H
