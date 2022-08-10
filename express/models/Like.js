const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");

const LikeSchema = mongoose.Schema({
  user: {
    type: ObjectId,
    required: true,
  },
  post: {
    type: ObjectId,
    required: true,
  },
  doesLike: {
    type: Boolean,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Likes", LikeSchema);
