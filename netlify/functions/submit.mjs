export default async (req) => {
  // Only allow POST requests
  if (req.method !== "POST") {
    return Response.json(
      {
        status: "error",
        message: "Method not allowed. Use POST.",
      },
      { status: 405 }
    );
  }

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_KEY;

  // Check Supabase configuration
  if (!supabaseUrl || !supabaseKey) {
    return Response.json(
      {
        status: "error",
        message: "Supabase environment variables are not configured.",
      },
      { status: 500 }
    );
  }

  // Read JSON body
  let data;

  try {
    data = await req.json();
  } catch {
    return Response.json(
      {
        status: "error",
        message: "Invalid JSON body.",
      },
      { status: 400 }
    );
  }

  // Get kheed
  const kheed = data?.kheed;

  if (!kheed) {
    return Response.json(
      {
        status: "error",
        message: "Missing 'kheed'.",
      },
      { status: 400 }
    );
  }

  // Send data to Supabase
  try {
    const response = await fetch(
      `${supabaseUrl}/rest/v1/claimtoken`,
      {
        method: "POST",
        headers: {
          apikey: supabaseKey,
          "Content-Type": "application/json",
          Prefer: "return=representation",
        },
        body: JSON.stringify({
          kheed: kheed,
        }),
      }
    );

    const responseText = await response.text();

    if (!response.ok) {
      return Response.json(
        {
          status: "failed",
          details: responseText,
        },
        { status: response.status }
      );
    }

    return Response.json(
      {
        status: "success",
        inserted: {
          kheed: kheed,
        },
      },
      { status: response.status }
    );
  } catch (error) {
    return Response.json(
      {
        status: "error",
        message: "Could not connect to Supabase.",
        details: error.message,
      },
      { status: 502 }
    );
  }
};
