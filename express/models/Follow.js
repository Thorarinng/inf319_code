const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");

const FollowSchema = mongoose.Schema({
  source: {
    // user ObjectId
    type: ObjectId,
    required: true,
  },
  destination: {
    // user ObjectId
    type: ObjectId,
    required: true,
  },
  isFollowing: {
    type: Boolean,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model("Follows", FollowSchema);
