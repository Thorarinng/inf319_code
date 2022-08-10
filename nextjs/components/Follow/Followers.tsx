import React from "react";

export const Followers = (props: { followers: any }) => {
  const { followers } = props;
  return (
    <div>
      <strong>Followers: </strong>
      {followers.length}
    </div>
  );
};
