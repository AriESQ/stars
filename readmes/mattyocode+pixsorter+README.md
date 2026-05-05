# PixSorter - Using algorithms to sort images

This web app provides a chance to explore foundational sorting algorithms in a practical context, while allowing users to view images in an unusual and interesting new way.

## Tech stack

- Typescript
- Next JS
- Sass
- Framer Motion
- Jest
- React Testing Library

## Deployment

Website is hosted on Vercel, and is available at [pixsorter.com](https://pixsorter.com)

![Homepage image](https://github.com/mattyocode/images/blob/main/pixsorter/pixsorter-main.png)

## How to install

1. Clone from Github

   ```bash
   cd projects
   git clone <repo-tag>
   ```

2. Add environment variables

   Create `.env` file in the root directory that includes the required variables for Unsplash API.

3. Install dependencies

   Run `yarn install` to install dependencies.

4. Run tests

   Run `yarn test` see results of unit tests.

5. Start app locally

   Run `yarn start` to launch the app on localhost:3000

## Key site features

### Sorting algorithms passed via context with shared interface

To allow for easy switching between algorithms, they share a common interface and are passed via context to the function that renders the pixel array (periodically) to the screen.

Algorithm interface

```tsx
export type SortAlgoTypes = (
  array: Uint8ClampedArray,
  sortedCallback: () => void,
  compare: compareFnTypes,
  sortPosition: number | SortDataTypes | null,
  pixelIdxLength?: number,
  renderLoops?: number
) => number | SortDataTypes;
```

Animation function in Canvas component

```tsx
const draw = useCallback(() => {
  const finishedSorting = () => {
    setIsSorted(true);
    setKeepSorting(false);
  };
  if (keepSorting && !isSorted) {
    if (imgData.current?.data && context.current) {
      // Algorithm will run for a set number of loops
      // before rendering to the screen
      let updatedPositionData = algorithm(
        imgData.current.data,
        finishedSorting,
        sortBy,
        sortPosition
      );
      setSortPosition(updatedPositionData);
      context.current.putImageData(imgData.current, 0, 0);
      requestId.current = requestAnimationFrame(draw);
    }
  }
  [...]
},[...]);
```

### Side-scrolling selection component

![Controls image](https://github.com/mattyocode/images/blob/main/pixsorter/controls.png)

The sideways selector component provides fluid user interaction through using Framer Motion's `easeInOut` transition animation for revealing hidden content, by and smoothly scrolling to the position of the selected value by passing down a reference to the parent container to the FieldValue component.

```tsx
const FieldValue = ({
  value,
  active,
  parentRef,
}: {
  value: string;
  active: boolean;
  parentRef: RefObject<HTMLElement>;
}) => {
  const optionRef = useRef<HTMLLIElement>(null);

  useEffect(() => {
    if (active && optionRef.current && parentRef?.current) {
      parentRef.current.scrollTo({
        left: optionRef.current.offsetLeft - optionRef.current.clientWidth,
        behavior: "smooth",
      });
    }
  }, [active, parentRef]);

  return (
    <li ref={optionRef} className={styles.fieldListItem}>
      {value}
    </li>
  );
};
```

## Challenges and Improvements

Algorithm pacing is a challenge, especially for the faster algorithms. Merge sort needs to be slowed down.

There's also more testing to be done. And a couple of other algorithms to add.

Next I'd like to implement K-means clustering to find and visualise the most common colours in an image - perhaps as a microservice that's called by the client.
