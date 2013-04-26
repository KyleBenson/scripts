#include <boost/geometry.hpp>
#include <boost/geometry/extensions/index/rtree/rtree.hpp>
 
#include <random>
 
#include <iostream>
#include <exception>
 
int main() try{
 
  typedef char value;
  typedef double coordinate_type;
  //typedef boost::geometry::model::d2::point_xy<coordinate_type> point;
  const size_t dimension = 2;
  typedef boost::geometry::cs::cartesian coordinate_system_type;
  typedef boost::geometry::model::point<coordinate_type, dimension, coordinate_system_type> point;
  typedef boost::geometry::model::box<point> box;
  typedef boost::geometry::index::rtree<box, value> rtree;
 
  std::mt19937_64 random_engine;
  std::uniform_real_distribution<coordinate_type> random_distribution_coordinate(0.0, 1.0);
  std::uniform_int_distribution<value> random_distribution_value('A', 'Z');
  auto random_point = [&](){return point(random_distribution_coordinate(random_engine), random_distribution_coordinate(random_engine));};
  auto random_value = [&](){return random_distribution_value(random_engine);};
  
  rtree r(16,4);
  
  r.print();
 
  for(auto n = 0; n < 10; ++n)
    r.insert( box(random_point(), random_point()), random_value() );
  
  r.print();
 
  std::cerr<<"---[find]---\n";
  for(const auto& v: r.find(box(point(0.25, 0.25), point(0.75, 0.75))))
    std::cerr<<v<<"\n";
 
 }catch(std::exception e){
 
  std::cerr<<e.what();
 
 }
