socialMedia = set ()                # Initializes an empty set called socialMedias.

socialMedia.add("Instagram")        # Adds the string "Instagram" to the set.
socialMedia.add("Snapchat")         # Adds the string "Snapchat" to the set.

socialMedia.add("Facebook")         # Adds the string "Facebook" to the set.
socialMedia.add("Facebook")         # sets do not allow duplicate elements, it has no effect.
socialMedia.remove("Facebook")      # Removes the string "Facebook" from the set.

print(len(socialMedia))             # the set contains "Instagram" and "Snapchat".
                                    # Display 2