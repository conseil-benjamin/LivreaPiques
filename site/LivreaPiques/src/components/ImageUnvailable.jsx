function ImageUnvailable({
    height,
    width
}) {
    console.log(height)
    return (
        <div style={{
            width: width,
            height: height,
            backgroundColor: "#f8d7da",
            color: "#721c24",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "8px",
            fontSize: "12px",
            padding: "5px",
            textAlign: "center"
        }}>
            Image indisponible
        </div>
    );
}

export default ImageUnvailable;
