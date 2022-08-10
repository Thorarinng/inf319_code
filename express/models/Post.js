const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");

const PostSchema = mongoose.Schema({
  user: {
    type: ObjectId,
    required: true,
  },
  likes: {
    type: [ObjectId],
  },
  parent: {
    type: ObjectId,
  },
  comment: {
    type: String,
    required: true,
  },
  likeCount: {
    type: Number,
    default: 0,
  },
  date: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Posts", PostSchema);
