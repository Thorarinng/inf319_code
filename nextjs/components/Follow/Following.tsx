import React from "react";

export const Following = (props: { following: any }) => {
  const { following } = props;
  return (
    <div>
      <strong>Following: </strong>
      {following.length}
    </div>
  );
};
