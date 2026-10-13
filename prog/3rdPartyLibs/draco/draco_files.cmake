set(FILES
  core/bit_utils.cc
  core/bounding_box.cc
  core/data_buffer.cc
  core/decoder_buffer.cc
  core/draco_types.cc
  core/encoder_buffer.cc
  core/options.cc
  core/quantization_utils.cc
  core/status.cc

  attributes/geometry_attribute.cc
  attributes/point_attribute.cc
  attributes/attribute_transform.cc
  attributes/attribute_quantization_transform.cc
  attributes/attribute_octahedron_transform.cc

  mesh/corner_table.cc
  mesh/mesh.cc
  mesh/mesh_attribute_corner_table.cc
  mesh/mesh_features.cc
  mesh/mesh_misc_functions.cc
  mesh/mesh_utils.cc
  mesh/triangle_soup_mesh_builder.cc

  point_cloud/point_cloud.cc
  point_cloud/point_cloud_builder.cc

  compression/decode.cc
  compression/draco_compression_options.cc
  compression/entropy/symbol_decoding.cc
  compression/entropy/shannon_entropy.cc
  compression/bit_coders/direct_bit_decoder.cc
  compression/bit_coders/rans_bit_decoder.cc
  compression/bit_coders/adaptive_rans_bit_decoder.cc
  compression/bit_coders/symbol_bit_decoder.cc
  compression/attributes/attributes_decoder.cc
  compression/attributes/sequential_attribute_decoder.cc
  compression/attributes/sequential_attribute_decoders_controller.cc
  compression/attributes/sequential_integer_attribute_decoder.cc
  compression/attributes/sequential_normal_attribute_decoder.cc
  compression/attributes/sequential_quantization_attribute_decoder.cc
  compression/attributes/kd_tree_attributes_decoder.cc
  compression/mesh/mesh_decoder.cc
  compression/mesh/mesh_edgebreaker_decoder.cc
  compression/mesh/mesh_edgebreaker_decoder_impl.cc
  compression/mesh/mesh_sequential_decoder.cc
  compression/point_cloud/point_cloud_decoder.cc
  compression/point_cloud/point_cloud_sequential_decoder.cc
  compression/point_cloud/point_cloud_kd_tree_decoder.cc
  compression/point_cloud/algorithms/integer_points_kd_tree_decoder.cc
  compression/point_cloud/algorithms/dynamic_integer_points_kd_tree_decoder.cc
  compression/point_cloud/algorithms/float_points_tree_decoder.cc

  metadata/geometry_metadata.cc
  metadata/metadata.cc
  metadata/metadata_decoder.cc
)
